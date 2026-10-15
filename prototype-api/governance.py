"""Configuração versionada, acompanhamento e retenção do protótipo local."""
import json
import hashlib
import math
from datetime import date, datetime, timedelta, timezone

SATISFACTION_ITEM_VERSION = "satisfacao-etapa-v1"
CES_ITEM_VERSION = "ces-facilidade-etapa-v1"


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def add_column(conn, table, name, definition):
    if name not in {row["name"] for row in conn.execute(f"pragma table_info({table})")}:
        conn.execute(f"alter table {table} add column {name} {definition}")


def initialize(conn):
    add_column(conn, "services", "configuration_version", "integer not null default 1")
    add_column(conn, "services", "duration_multiplier", "real not null default 1.5")
    add_column(conn, "admin_alerts", "configuration_version", "integer")
    add_column(conn, "sessions", "telemetry_allowed", "integer not null default 0")
    add_column(conn, "sessions", "notice_version", "text")
    conn.executescript("""
        create table if not exists service_config_versions (
            id integer primary key autoincrement,
            service_id text not null, version integer not null,
            click_threshold integer not null, average_duration_seconds integer not null,
            duration_multiplier real not null, reason text not null,
            actor text not null, created_at text not null, unique(service_id, version)
        );
        create table if not exists improvement_actions (
            id integer primary key autoincrement, service_id text not null,
            evidence_type text not null, baseline_json text not null,
            insight text not null, improvement text not null, owner_role text not null,
            due_date text, status text not null default 'aberta',
            created_at text not null, updated_at text not null
        );
        create table if not exists improvement_history (
            id integer primary key autoincrement, action_id integer not null,
            status text not null, note text not null, snapshot_json text not null,
            created_at text not null
        );
    """)


def seed_history(conn):
    conn.execute("""insert or ignore into service_config_versions
        (service_id, version, click_threshold, average_duration_seconds,
         duration_multiplier, reason, actor, created_at)
        select id, configuration_version, click_threshold, average_duration_seconds,
               duration_multiplier, 'Configuração inicial preservada', 'sistema', ? from services""",
                 (timestamp(),))


def integer(value, field, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{field} deve ser inteiro entre {minimum} e {maximum}")
    return value


def text(value, field, minimum=1, maximum=1000):
    if not isinstance(value, str) or not minimum <= len(value.strip()) <= maximum:
        raise ValueError(f"{field} deve ter entre {minimum} e {maximum} caracteres")
    return value.strip()


def update_configuration(conn, payload):
    service_id = text(payload.get("service_id"), "service_id", maximum=80)
    current = conn.execute("select * from services where id=?", (service_id,)).fetchone()
    if current is None:
        raise ValueError("Serviço inexistente")
    expected = integer(payload.get("expected_version"), "expected_version", 1, 1000000)
    clicks = integer(payload.get("click_threshold"), "click_threshold", 1, 10000)
    duration = integer(payload.get("average_duration_seconds"), "average_duration_seconds", 1, 86400)
    multiplier = payload.get("duration_multiplier")
    if type(multiplier) not in (int, float) or not math.isfinite(multiplier) or not 1 <= multiplier <= 10:
        raise ValueError("duration_multiplier deve ser número finito entre 1 e 10")
    reason = text(payload.get("reason"), "reason", 10, 500)
    changed = conn.execute("""update services set click_threshold=?, average_duration_seconds=?,
        duration_multiplier=?, configuration_version=configuration_version+1
        where id=? and configuration_version=?""", (clicks, duration, multiplier, service_id, expected))
    if changed.rowcount != 1:
        raise ConfigurationConflict("Configuração modificada; recarregue antes de salvar")
    conn.execute("""insert into service_config_versions
        (service_id, version, click_threshold, average_duration_seconds, duration_multiplier,
         reason, actor, created_at) values (?,?,?,?,?,?,?,?)""",
                 (service_id, expected + 1, clicks, duration, multiplier, reason, "administrador-local", timestamp()))
    return dict(conn.execute("select * from services where id=?", (service_id,)).fetchone())


class ConfigurationConflict(ValueError):
    pass


def snapshot(conn, service_id):
    row = conn.execute("""select count(*) as feedbacks,
        count(case when ces_item_version=? then ces end) as ces_n,
        round(avg(case when ces_item_version=? then ces end),2) as ces_mean,
        count(case when stars_item_version=? then stars end) as satisfaction_n,
        round(avg(case when stars_item_version=? then stars end),2) as satisfaction_mean
        from feedbacks where service_id=?""",
        (CES_ITEM_VERSION, CES_ITEM_VERSION, SATISFACTION_ITEM_VERSION, SATISFACTION_ITEM_VERSION, service_id)).fetchone()
    traits = {}
    for entry in conn.execute("select traits_json from feedbacks where service_id=?", (service_id,)):
        for trait in set(json.loads(entry[0])):
            traits[trait] = traits.get(trait, 0) + 1
    return {**dict(row), "attributes": traits, "ces_version": CES_ITEM_VERSION,
            "satisfaction_version": SATISFACTION_ITEM_VERSION,
            "alerts": conn.execute("select count(*) from admin_alerts where service_id=?", (service_id,)).fetchone()[0],
            "measured_at": timestamp(), "meaning": "Agregado descritivo; não prova causa ou efeito da ação"}


def create_improvement(conn, payload):
    if not conn.in_transaction:
        conn.execute("begin immediate")
    service = text(payload.get("service_id"), "service_id", maximum=80)
    if conn.execute("select id from services where id=?", (service,)).fetchone() is None:
        raise ValueError("Serviço inexistente")
    evidence = payload.get("evidence_type")
    if evidence not in {"ces", "satisfacao", "alertas", "atributos", "outro"}:
        raise ValueError("Tipo de evidência inválido")
    insight = text(payload.get("insight"), "insight", 10)
    improvement = text(payload.get("improvement"), "improvement", 10)
    role = text(payload.get("owner_role"), "owner_role", 2, 80)
    due = payload.get("due_date") or None
    if due is not None:
        if not isinstance(due, str):
            raise ValueError("Prazo deve ser uma data ISO")
        date.fromisoformat(due)
    baseline = json.dumps(snapshot(conn, service), ensure_ascii=False)
    now = timestamp()
    cursor = conn.execute("""insert into improvement_actions
        (service_id,evidence_type,baseline_json,insight,improvement,owner_role,due_date,created_at,updated_at)
        values (?,?,?,?,?,?,?,?,?)""", (service, evidence, baseline, insight, improvement, role, due, now, now))
    conn.execute("""insert into improvement_history (action_id,status,note,snapshot_json,created_at)
        values (?, 'aberta', 'Ação criada', ?, ?)""", (cursor.lastrowid, baseline, now))
    return cursor.lastrowid


def update_improvement(conn, payload):
    if not conn.in_transaction:
        conn.execute("begin immediate")
    action_id = integer(payload.get("action_id"), "action_id", 1, 1000000000)
    row = conn.execute("select * from improvement_actions where id=?", (action_id,)).fetchone()
    if row is None:
        raise ValueError("Ação inexistente")
    status = payload.get("status")
    if status not in {"aberta", "em_andamento", "concluida"}:
        raise ValueError("Situação inválida")
    note = text(payload.get("note"), "note", 10)
    now = timestamp()
    followup = json.dumps(snapshot(conn, row["service_id"]), ensure_ascii=False)
    conn.execute("update improvement_actions set status=?, updated_at=? where id=?", (status, now, action_id))
    conn.execute("""insert into improvement_history (action_id,status,note,snapshot_json,created_at)
        values (?,?,?,?,?)""", (action_id, status, note, followup, now))
    return action_id


def list_improvements(conn):
    result = []
    for row in conn.execute("select * from improvement_actions order by id desc"):
        item = dict(row)
        item["baseline"] = json.loads(item.pop("baseline_json"))
        item["history"] = []
        for history in conn.execute("select * from improvement_history where action_id=? order by id", (item["id"],)):
            entry = dict(history)
            entry["snapshot"] = json.loads(entry.pop("snapshot_json"))
            item["history"].append(entry)
        result.append(item)
    return result


def purge_expired(conn, days, confirm=False, cutoff=None, expected_token=None):
    integer(days, "retention_days", 1, 3650)
    boundary = datetime.now(timezone.utc) - timedelta(days=days)
    if cutoff is None:
        cutoff = boundary.isoformat()
    if not isinstance(cutoff, str):
        raise ValueError("Corte de retenção inválido")
    parsed = datetime.fromisoformat(cutoff)
    if parsed.tzinfo is None or parsed > boundary:
        raise ValueError("Corte de retenção inválido")
    if not conn.in_transaction:
        conn.execute("begin immediate" if confirm else "begin")
    result = {"cutoff": cutoff, "retention_days": days, "executed": confirm, "counts": {}}
    for table in ["click_events", "page_time_events", "admin_alerts", "feedbacks"]:
        result["counts"][table] = conn.execute(f"select count(*) from {table} where created_at < ?", (cutoff,)).fetchone()[0]
    # Simular as referências que permanecerão, tanto na prévia quanto na execução.
    condition = """last_seen_at < ? and id not in (
        select session_id from click_events where created_at >= ? union
        select session_id from page_time_events where created_at >= ? union
        select session_id from admin_alerts where created_at >= ? union
        select session_id from feedbacks where created_at >= ?)"""
    result["counts"]["sessions"] = conn.execute("select count(*) from sessions where " + condition, (cutoff,) * 5).fetchone()[0]
    closed = "status='concluida' and updated_at < ?"
    result["counts"]["improvement_actions"] = conn.execute("select count(*) from improvement_actions where " + closed, (cutoff,)).fetchone()[0]
    result["counts"]["improvement_history"] = conn.execute("select count(*) from improvement_history where action_id in (select id from improvement_actions where " + closed + ")", (cutoff,)).fetchone()[0]
    # A prévia vincula os registros e seu conteúdo, não somente as contagens.
    # O resumo é opaco: não devolvemos IDs ou dados pessoais na prévia.
    digest = hashlib.sha256()
    targets = [(table, "created_at < ?", (cutoff,))
               for table in ["click_events", "page_time_events", "admin_alerts", "feedbacks"]]
    targets += [("sessions", condition, (cutoff,) * 5),
                ("improvement_actions", closed, (cutoff,)),
                ("improvement_history", "action_id in (select id from improvement_actions where " + closed + ")", (cutoff,))]
    for table, predicate, params in targets:
        digest.update((table + "\n").encode())
        for row in conn.execute(f"select * from {table} where {predicate} order by id", params):
            digest.update(json.dumps(dict(row), ensure_ascii=False, sort_keys=True).encode())
            digest.update(b"\n")
    token = hashlib.sha256(json.dumps({"cutoff": cutoff, "counts": result["counts"],
                                      "records_digest": digest.hexdigest()}, sort_keys=True).encode()).hexdigest()
    result["preview_token"] = token
    if confirm:
        if expected_token != token:
            raise ConfigurationConflict("A prévia mudou ou não foi informada; consulte novamente")
        for table in ["click_events", "page_time_events", "admin_alerts", "feedbacks"]:
            conn.execute(f"delete from {table} where created_at < ?", (cutoff,))
        conn.execute("delete from sessions where " + condition, (cutoff,) * 5)
        conn.execute("delete from improvement_history where action_id in (select id from improvement_actions where " + closed + ")", (cutoff,))
        conn.execute("delete from improvement_actions where " + closed, (cutoff,))
    return result
