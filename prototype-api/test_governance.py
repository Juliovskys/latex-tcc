"""Verificações de gestão e proteção local, usando somente dados sintéticos."""
import json
import unittest
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import test_feedback_ces as base

app = base.app


class GovernanceTest(unittest.TestCase):
    setUp = base.FeedbackCESTest.setUp
    tearDown = base.FeedbackCESTest.tearDown
    request = base.FeedbackCESTest.request
    feedback = base.FeedbackCESTest.feedback

    def configuration(self, **fields):
        return self.request("/api/admin/configurations", {
            "service_id": "imposto-renda", "expected_version": 1,
            "click_threshold": 2, "average_duration_seconds": 20,
            "duration_multiplier": 2, "reason": "Ajuste operacional de demonstração", **fields})

    def permission(self):
        return self.request("/api/session/permission", {
            "session_id": "synthetic-test", "allow": True, "notice_version": app.NOTICE_VERSION})

    def click(self, **fields):
        return self.request("/api/events/click", {
            "session_id": "synthetic-test", "service_id": "imposto-renda", "page_id": "servico-imposto-renda", **fields})

    def test_configuration_survives_restart_and_rejects_lost_update(self):
        self.assertEqual(self.configuration()[0], 200)
        app.init_db()
        self.assertEqual(app.get_service_by_id("imposto-renda")["click_threshold"], 2)
        self.assertEqual(app.get_service_by_id("imposto-renda")["configuration_version"], 2)
        self.assertEqual(self.configuration(click_threshold=8)[0], 409)
        _, history = self.request("/api/admin/configurations")
        own = [row for row in history if row["service_id"] == "imposto-renda"]
        self.assertEqual([row["version"] for row in own], [2, 1])
        self.assertEqual(len({row["service_id"] for row in history}), 3)

    def test_invalid_configuration_does_not_create_a_version(self):
        for fields in [{"click_threshold": 0}, {"click_threshold": True},
                       {"average_duration_seconds": -1}, {"duration_multiplier": float("nan")},
                       {"duration_multiplier": 0.1}, {"reason": "curta"}]:
            with self.subTest(fields=fields):
                self.assertEqual(self.configuration(**fields)[0], 400)
        self.assertEqual(app.get_service_by_id("imposto-renda")["configuration_version"], 1)

    def test_rule_uses_new_configuration_and_records_version(self):
        self.configuration()
        self.permission()
        self.assertEqual(self.click()[1]["actions"], [])
        self.assertEqual(self.click()[1]["actions"], [])
        self.assertTrue(self.click()[1]["actions"])
        _, alerts = self.request("/api/admin/alerts")
        self.assertEqual(alerts[0]["configuration_version"], 2)
        self.assertNotIn("silent", alerts[0])
        with app.connect() as conn:
            actions = app.evaluate_duration_actions(conn, "synthetic-test", "imposto-renda", 40)
            self.assertEqual(actions, [])
            self.assertTrue(app.evaluate_duration_actions(conn, "synthetic-test", "imposto-renda", 41))

    def test_opt_in_withdrawal_and_minimization(self):
        self.assertEqual(self.click()[0], 403)
        self.assertEqual(self.permission()[0], 200)
        self.assertEqual(self.click(url="https://example.test/private?cpf=123")[0], 400)
        self.assertEqual(self.click(user_id="identity")[0], 400)
        self.assertEqual(self.click(x=1)[0], 400)
        self.assertEqual(self.click(y=2)[0], 400)
        self.assertEqual(self.click(x=1, y=2)[0], 400)
        self.assertEqual(self.click()[0], 201)
        status, normalized = self.click(session_id=" synthetic-test ")
        self.assertEqual(status, 201)
        self.assertEqual(normalized["session_id"], "synthetic-test")
        with app.connect() as conn:
            self.assertEqual(conn.execute("select count(*) from sessions").fetchone()[0], 1)
        self.request("/api/session/withdraw", {"session_id": "synthetic-test"})
        self.assertEqual(self.click()[0], 403)
        self.assertEqual(self.request("/api/events/page-time", {
            "session_id": "synthetic-test", "service_id": "imposto-renda", "duration_seconds": 120})[0], 403)
        with app.connect() as conn:
            row = conn.execute("select user_id,url,x,y from click_events").fetchone()
            self.assertEqual(tuple(row), (None, None, None, None))
        # Avaliação voluntária independe da permissão de telemetria.
        self.assertEqual(self.feedback(ces=5)[0], 201)

    def test_administrative_routes_require_key_and_health_hides_path(self):
        for path in ["/api/admin/dashboard", "/api/admin/alerts", "/api/admin/configurations",
                     "/api/admin/improvements", "/api/admin/retention"]:
            with self.subTest(path=path):
                with self.assertRaises(HTTPError) as failure:
                    urlopen(self.url + path)
                self.assertEqual(failure.exception.code, 401)
        with self.assertRaises(HTTPError) as failure:
            urlopen(Request(self.url + "/api/admin/configurations", data=b"{}",
                            headers={"Content-Type": "application/json"}))
        self.assertEqual(failure.exception.code, 401)
        _, health = self.request("/health")
        self.assertNotIn("database", health)
        with self.assertRaises(HTTPError) as failure:
            urlopen(Request(self.url + "/api/feedback", data=b"{}", headers={
                "Content-Type": "application/json", "Origin": "https://external.test"}))
        self.assertEqual(failure.exception.code, 403)

    def test_action_has_immutable_baseline_and_followup_history(self):
        self.feedback(ces=2)
        status, created = self.request("/api/admin/improvements", {
            "service_id": "imposto-renda", "evidence_type": "ces",
            "insight": "Investigar dificuldade na orientação", "improvement": "Revisar a explicação da etapa",
            "owner_role": "Equipe de conteúdo", "due_date": "2026-12-01"})
        self.assertEqual(status, 201)
        action_id = created["action_id"]
        self.feedback(ces=6)
        self.assertEqual(self.request("/api/admin/improvements", {
            "action_id": action_id, "status": "concluida", "note": ""})[0], 400)
        self.assertEqual(self.request("/api/admin/improvements", {
            "action_id": action_id, "status": "concluida", "note": "Observação sintética de acompanhamento"})[0], 201)
        _, actions = self.request("/api/admin/improvements")
        self.assertEqual(actions[0]["baseline"]["ces_mean"], 2)
        self.assertEqual(actions[0]["baseline"]["ces_n"], 1)
        self.assertEqual(actions[0]["history"][-1]["snapshot"]["ces_mean"], 4)
        self.assertEqual(len(actions[0]["history"]), 2)

    def test_retention_preview_then_confirmed_purge(self):
        self.feedback(ces=3)
        self.feedback(ces=7, session_id="recent")
        with app.connect() as conn:
            conn.execute("update feedbacks set created_at='2020-01-01' where session_id='synthetic-test'")
            conn.execute("update sessions set last_seen_at='2020-01-01' where id='synthetic-test'")
        _, preview = self.request("/api/admin/retention")
        self.assertFalse(preview["executed"])
        self.assertEqual(preview["counts"]["feedbacks"], 1)
        self.assertEqual(preview["counts"]["sessions"], 1)
        self.assertEqual(self.request("/api/admin/retention", {"confirm": False})[0], 400)
        self.assertEqual(self.request("/api/admin/retention", {
            "confirm": True, "cutoff": preview["cutoff"], "preview_token": preview["preview_token"]})[0], 200)
        with app.connect() as conn:
            self.assertEqual(conn.execute("select count(*) from feedbacks").fetchone()[0], 1)
            self.assertEqual(conn.execute("select id from sessions").fetchone()[0], "recent")

    def test_unknown_item_versions_are_not_pooled(self):
        self.feedback(ces=1)
        with app.connect() as conn:
            conn.execute("update feedbacks set ces_item_version='other', stars_item_version='other'")
        _, dashboard = self.request("/api/admin/dashboard")
        row = dashboard["feedback_metrics"][0]
        self.assertIsNone(row["average_ces"])
        self.assertIsNone(row["average_stars"])
        self.assertEqual(row["ces_other_versions"], 1)
        self.assertEqual(row["ces_missing"], 0)
        self.assertEqual(sum(row["ces_distribution"].values()), 0)

    def test_retention_conflict_and_closed_action_lifecycle(self):
        self.feedback(ces=3)
        _, action = self.request("/api/admin/improvements", {
            "service_id": "imposto-renda", "evidence_type": "ces",
            "insight": "Hipótese sintética para investigar", "improvement": "Revisar as instruções da etapa",
            "owner_role": "Equipe de conteúdo"})
        self.request("/api/admin/improvements", {
            "action_id": action["action_id"], "status": "concluida", "note": "Ação sintética concluída para ensaio"})
        with app.connect() as conn:
            conn.execute("update improvement_actions set updated_at='2020-01-01'")
        _, preview = self.request("/api/admin/retention")
        self.assertEqual(preview["counts"]["improvement_actions"], 1)
        self.assertEqual(preview["counts"]["improvement_history"], 2)
        with app.connect() as conn:
            conn.execute("update feedbacks set created_at='2020-01-01'")
        payload = {"confirm": True, "cutoff": preview["cutoff"], "preview_token": preview["preview_token"]}
        self.assertEqual(self.request("/api/admin/retention", payload)[0], 409)
        with app.connect() as conn:
            self.assertEqual(conn.execute("select count(*) from improvement_actions").fetchone()[0], 1)
        _, preview = self.request("/api/admin/retention")
        payload.update(cutoff=preview["cutoff"], preview_token=preview["preview_token"])
        self.assertEqual(self.request("/api/admin/retention", payload)[0], 200)
        with app.connect() as conn:
            self.assertEqual(conn.execute("select count(*) from improvement_history").fetchone()[0], 0)

    def test_duration_rejects_non_numbers_and_non_finite_values(self):
        self.permission()
        for value in [True, "120", None, -1, 86401, float("nan"), float("inf")]:
            with self.subTest(value=value):
                self.assertEqual(self.request("/api/events/page-time", {
                    "session_id": "synthetic-test", "service_id": "imposto-renda",
                    "duration_seconds": value})[0], 400)
        with app.connect() as conn:
            self.assertEqual(conn.execute("select count(*) from page_time_events").fetchone()[0], 0)

    def test_input_boundaries_and_feedback_html_escaping(self):
        self.assertEqual(self.feedback(stars=True)[0], 400)
        self.assertEqual(self.feedback(traits=["unrecognized"])[0], 400)
        self.assertEqual(self.feedback(comment="x" * 2001)[0], 400)
        self.assertEqual(self.feedback(user_id="civil-identification")[0], 400)
        query = urlencode({"session_id": '</script><script>alert(1)</script>', "service_id": "imposto-renda"})
        with urlopen(self.url + "/feedback?" + query) as response:
            html = response.read().decode()
        self.assertNotIn('</script><script>alert(1)</script>', html)
        self.assertIn('\\u003c/script', html)

    def test_retention_detects_changed_records_with_unchanged_counts(self):
        self.feedback(ces=3)
        with app.connect() as conn:
            conn.execute("update feedbacks set created_at='2020-01-01'")
            old_id = conn.execute("select id from feedbacks").fetchone()[0]
        _, preview = self.request("/api/admin/retention")
        # Substituir por outra linha vencida, mantendo a contagem e a sessão.
        self.feedback(ces=6)
        with app.connect() as conn:
            conn.execute("delete from feedbacks where id=?", (old_id,))
            conn.execute("update feedbacks set created_at='2020-01-01'")
        _, replaced = self.request("/api/admin/retention")
        self.assertEqual(preview["counts"], replaced["counts"])
        payload = {"confirm": True, "cutoff": preview["cutoff"], "preview_token": preview["preview_token"]}
        self.assertEqual(self.request("/api/admin/retention", payload)[0], 409)
        # Alterar conteúdo mantendo também o mesmo ID deve invalidar a prévia.
        with app.connect() as conn:
            conn.execute("update feedbacks set comment='Conteúdo sintético alterado'")
        payload.update(cutoff=replaced["cutoff"], preview_token=replaced["preview_token"])
        self.assertEqual(self.request("/api/admin/retention", payload)[0], 409)
        with app.connect() as conn:
            self.assertEqual(conn.execute("select count(*) from feedbacks").fetchone()[0], 1)
        _, latest = self.request("/api/admin/retention")
        payload.update(cutoff=latest["cutoff"], preview_token=latest["preview_token"])
        self.assertEqual(self.request("/api/admin/retention", payload)[0], 200)


if __name__ == "__main__":
    unittest.main()
