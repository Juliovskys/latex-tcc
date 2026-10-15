"""Verificação técnica do CES. Dados sintéticos, sem avaliação com cidadãos."""
import importlib.util
import json
import sqlite3
import tempfile
import threading
import unittest
from contextlib import closing
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


spec = importlib.util.spec_from_file_location("prototype_server", Path(__file__).with_name("server.py"))
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class FeedbackCESTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.previous_path = app.DB_PATH
        app.DB_PATH = Path(self.directory.name) / "test.db"
        app.init_db()
        self.http = ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
        self.thread = threading.Thread(target=self.http.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.http.server_port}"

    def tearDown(self):
        self.http.shutdown()
        self.http.server_close()
        self.thread.join()
        app.DB_PATH = self.previous_path
        self.directory.cleanup()

    def request(self, path, payload=None):
        headers = {"Content-Type": "application/json"}
        if path.startswith("/api/admin/"):
            headers["Authorization"] = "Bearer " + app.ADMIN_TOKEN
        req = Request(self.url + path, headers=headers,
                      data=json.dumps(payload).encode() if payload is not None else None)
        try:
            with urlopen(req) as response:
                return response.status, json.loads(response.read())
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def feedback(self, **fields):
        payload = {"session_id": "synthetic-test", "service_id": "imposto-renda",
                   "stars": 4, "traits": [], **fields}
        return self.request("/api/feedback", payload)

    def test_optional_answers_and_all_seven_categories(self):
        for value in range(1, 8):
            with self.subTest(value=value):
                self.assertEqual(self.feedback(ces=value)[0], 201)
        self.assertEqual(self.feedback()[0], 201)
        self.assertEqual(self.feedback(ces=None)[0], 201)
        with app.connect() as conn:
            rows = conn.execute("select ces, ces_item_version from feedbacks order by id").fetchall()
        self.assertEqual([row["ces"] for row in rows], [1, 2, 3, 4, 5, 6, 7, None, None])
        self.assertTrue(all(row["ces_item_version"] == app.CES_ITEM_VERSION for row in rows[:7]))
        self.assertTrue(all(row["ces_item_version"] is None for row in rows[7:]))

    def test_invalid_values_are_rejected_without_creating_records(self):
        for value in [0, 8, -1, True, False, 2.5, "7", "", [], {}]:
            with self.subTest(value=value):
                self.assertEqual(self.feedback(ces=value)[0], 400)
        self.assertEqual(self.feedback(nps=9)[0], 400)
        with app.connect() as conn:
            self.assertEqual(conn.execute("select count(*) from feedbacks").fetchone()[0], 0)

    def test_dashboard_excludes_missing_values_and_separates_services(self):
        for value in [1, 4, 7, None]:
            self.assertEqual(self.feedback(ces=value)[0], 201)
        self.assertEqual(self.feedback(service_id="servico-publico-generico", ces=2)[0], 201)
        status, dashboard = self.request("/api/admin/dashboard")
        self.assertEqual(status, 200)
        rows = {row["service_id"]: row for row in dashboard["feedback_metrics"]}
        row = rows["imposto-renda"]
        self.assertEqual((row["ces_responses"], row["ces_missing"], row["average_ces"]), (3, 1, 4.0))
        self.assertEqual(row["ces_distribution"], {"1": 1, "2": 0, "3": 0, "4": 1, "5": 0, "6": 0, "7": 1})
        self.assertEqual(rows["servico-publico-generico"]["average_ces"], 2)
        self.assertNotIn("average_nps", row)
        self.assertEqual(dashboard["ces_instrument"]["version"], app.CES_ITEM_VERSION)
        self.assertTrue(dashboard["ces_instrument"]["optional"])

    def test_no_response_means_null_average(self):
        self.feedback()
        _, result = self.request("/api/admin/dashboard")
        row = result["feedback_metrics"][0]
        self.assertIsNone(row["average_ces"])
        self.assertEqual(row["ces_responses"], 0)
        self.assertEqual(row["ces_missing"], 1)
        self.assertEqual(sum(row["ces_distribution"].values()), 0)

    def test_migration_backs_up_originals_and_does_not_invent_ces(self):
        with app.connect() as conn:
            conn.execute("drop table feedbacks")
            conn.execute("""create table feedbacks (
                id integer primary key autoincrement, session_id text not null,
                user_id text, service_id text, stars integer not null,
                nps integer not null, traits_json text not null,
                comment text, created_at text not null)""")
            conn.execute("""insert into feedbacks values
                (17, 'historical', null, 'imposto-renda', 3, 10,
                 '["usabilidade"]', 'Comentário preservado', '2026-06-28')""")
        app.init_db()
        backups = list(Path(self.directory.name).glob("test.pre-ces-*.db"))
        self.assertEqual(len(backups), 1)
        with closing(sqlite3.connect(backups[0])) as backup:
            self.assertEqual(backup.execute("select nps, comment from feedbacks").fetchone(),
                             (10, "Comentário preservado"))
        with app.connect() as conn:
            columns = {row["name"] for row in conn.execute("pragma table_info(feedbacks)")}
            row = dict(conn.execute("select * from feedbacks where id = 17").fetchone())
        self.assertNotIn("nps", columns)
        self.assertEqual(row["comment"], "Comentário preservado")
        self.assertEqual(row["traits_json"], '["usabilidade"]')
        self.assertIsNone(row["ces"])
        self.assertIsNone(row["ces_item_version"])
        app.init_db()
        self.assertEqual(len(list(Path(self.directory.name).glob("test.pre-ces-*.db"))), 1)
        self.assertEqual(self.feedback(ces=7)[0], 201)
        with app.connect() as conn:
            self.assertEqual(conn.execute("select max(id) from feedbacks").fetchone()[0], 18)
        _, dashboard = self.request("/api/admin/dashboard")
        metric = dashboard["feedback_metrics"][0]
        self.assertEqual(metric["average_stars"], 4)
        self.assertEqual(metric["stars_responses"], 1)
        self.assertEqual(metric["stars_other_versions"], 1)
        self.assertEqual(metric["ces_responses"], 1)
        self.assertEqual(metric["ces_missing"], 1)
        self.assertEqual(metric["ces_missing_current_contract"], 0)
        self.assertEqual(metric["ces_missing_legacy_or_unknown"], 1)

    def test_dashboard_separates_current_missing_from_legacy_or_unknown(self):
        self.feedback(ces=5)
        self.feedback(ces=None)
        self.feedback(ces=None)
        with app.connect() as conn:
            conn.execute("update feedbacks set stars_item_version=null where id=(select max(id) from feedbacks)")
        _, dashboard = self.request("/api/admin/dashboard")
        metric = dashboard["feedback_metrics"][0]
        self.assertEqual(metric["total_feedbacks"], 3)
        self.assertEqual(metric["ces_responses"], 1)
        self.assertEqual(metric["average_ces"], 5)
        self.assertEqual(metric["ces_missing"], 2)
        self.assertEqual(metric["ces_missing_current_contract"], 1)
        self.assertEqual(metric["ces_missing_legacy_or_unknown"], 1)

    def test_form_has_optional_ces_and_preserves_missing_values(self):
        with urlopen(self.url + "/feedback?session_id=synthetic-test&service_id=imposto-renda") as response:
            html = response.read().decode("utf-8")
        self.assertIn(app.CES_QUESTION, html)
        self.assertIn('<select id="ces" name="ces" aria-describedby="ces-help">', html)
        self.assertIn('data.get("ces") === "" ? null', html)
        self.assertNotIn('id="nps"', html)
        self.assertIn('7 — Concordo totalmente', html)


if __name__ == "__main__":
    unittest.main()
