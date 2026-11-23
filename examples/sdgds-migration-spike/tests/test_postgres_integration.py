from __future__ import annotations

import os

import pytest
psycopg = pytest.importorskip("psycopg")

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATABASE_URL = os.getenv("SDGDS_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(
    not DATABASE_URL,
    reason="Set SDGDS_TEST_DATABASE_URL to a disposable PostgreSQL 16 database",
)


@pytest.fixture(scope="module", autouse=True)
def install_schema():
    if not DATABASE_URL:
        yield
        return
    ddl = (ROOT / "migrations" / "001_sdgds_postgres.sql").read_text(encoding="utf-8")
    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        # Destructive reset is restricted to the ephemeral CI service database.
        conn.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;", prepare=False)
        conn.execute(ddl, prepare=False)
    yield
    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        conn.execute(
            "TRUNCATE sdgds_term_relations, sdgds_term_aliases, sdgds_outbox_events, "
            "sdgds_audit_events, sdgds_terms CASCADE"
        )


@pytest.fixture(autouse=True)
def clean_tables():
    if not DATABASE_URL:
        yield
        return
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute(
            "TRUNCATE sdgds_term_relations, sdgds_term_aliases, sdgds_outbox_events, "
            "sdgds_audit_events, sdgds_terms CASCADE"
        )
    yield


def insert_term(conn, term_id="HSMART-0001", label="Capability", slug="capability"):
    conn.execute(
        """INSERT INTO sdgds_terms
           (term_id, canonical_label, slug, aliases, definition, status, domains, provenance)
           VALUES (%s, %s, %s, %s::jsonb, %s, %s, %s::jsonb, %s::jsonb)""",
        (
            term_id,
            label,
            slug,
            '["AI capability"]',
            "A synthetic canonical definition.",
            "Canonical",
            '["Registry & Capability"]',
            '{"source":"fixture://postgres-16"}',
        ),
    )


def test_postgres_16_installs_schema_and_preserves_hsmart_string_ids():
    with psycopg.connect(DATABASE_URL) as conn:
        insert_term(conn)
        row = conn.execute(
            "SELECT term_id, canonical_label, status, jsonb_typeof(provenance) "
            "FROM sdgds_terms WHERE term_id = %s",
            ("HSMART-0001",),
        ).fetchone()
        assert row == ("HSMART-0001", "Capability", "Canonical", "object")
        tables = conn.execute(
            """SELECT count(*) FROM information_schema.tables
               WHERE table_schema='public' AND table_name LIKE 'sdgds_%'"""
        ).fetchone()[0]
        assert tables == 5


def test_case_insensitive_unique_label_and_slug_constraints():
    with psycopg.connect(DATABASE_URL) as conn:
        insert_term(conn, "HSMART-0001", "Capability", "capability")
        with pytest.raises(psycopg.errors.UniqueViolation):
            insert_term(conn, "HSMART-0002", "CAPABILITY", "capability-two")
        conn.rollback()
        with pytest.raises(psycopg.errors.UniqueViolation):
            insert_term(conn, "HSMART-0003", "Different Label", "CAPABILITY")


def test_jsonb_status_and_term_id_constraints():
    with psycopg.connect(DATABASE_URL) as conn:
        with pytest.raises(psycopg.errors.CheckViolation):
            conn.execute(
                """INSERT INTO sdgds_terms
                   (term_id, canonical_label, slug, aliases, definition, status, domains, provenance)
                   VALUES ('HSMART-0001','Bad JSON','bad-json','{}','x','Canonical','[]','{}')"""
            )
        conn.rollback()
        with pytest.raises(psycopg.errors.CheckViolation):
            conn.execute(
                """INSERT INTO sdgds_terms
                   (term_id, canonical_label, slug, definition, status)
                   VALUES ('HSMART-0002','Bad Status','bad-status','x','Unknown')"""
            )
        conn.rollback()
        with pytest.raises(psycopg.errors.CheckViolation):
            conn.execute(
                """INSERT INTO sdgds_terms
                   (term_id, canonical_label, slug, definition, status)
                   VALUES ('x','Short ID','short-id','x','Proposed')"""
            )


def test_alias_relation_foreign_key_and_self_relation_constraints():
    with psycopg.connect(DATABASE_URL) as conn:
        insert_term(conn, "HSMART-0001", "Capability", "capability")
        insert_term(conn, "HSMART-0002", "Capability Version", "capability-version")
        conn.execute(
            "INSERT INTO sdgds_term_aliases(term_id, alias, language) VALUES (%s,%s,%s)",
            ("HSMART-0001", "AI capability", "English"),
        )
        with pytest.raises(psycopg.errors.ForeignKeyViolation):
            conn.execute(
                "INSERT INTO sdgds_term_aliases(term_id, alias) VALUES (%s,%s)",
                ("HSMART-9999", "orphan alias"),
            )
        conn.rollback()
        with pytest.raises(psycopg.errors.CheckViolation):
            conn.execute(
                """INSERT INTO sdgds_term_relations(source_term_id,target_term_id,relation_type)
                   VALUES (%s,%s,%s)""",
                ("HSMART-0001", "HSMART-0001", "parent"),
            )
        conn.rollback()
        with pytest.raises(psycopg.errors.CheckViolation):
            conn.execute(
                """INSERT INTO sdgds_term_relations(source_term_id,target_term_id,relation_type)
                   VALUES (%s,%s,%s)""",
                ("HSMART-0001", "HSMART-0002", "made_up_relation"),
            )


def test_outbox_idempotency_key_is_unique():
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute(
            """INSERT INTO sdgds_outbox_events
               (aggregate_type,aggregate_id,event_type,payload,idempotency_key)
               VALUES ('term','HSMART-0001','term.proposed','{"term_id":"HSMART-0001"}','idem-1')"""
        )
        with pytest.raises(psycopg.errors.UniqueViolation):
            conn.execute(
                """INSERT INTO sdgds_outbox_events
                   (aggregate_type,aggregate_id,event_type,payload,idempotency_key)
                   VALUES ('term','HSMART-0002','term.proposed','{"term_id":"HSMART-0002"}','idem-1')"""
            )


def test_term_audit_and_outbox_share_transaction_boundary():
    with psycopg.connect(DATABASE_URL) as conn:
        with pytest.raises(RuntimeError):
            with conn.transaction():
                insert_term(conn, "HSMART-0099", "Rolled Back", "rolled-back")
                conn.execute(
                    """INSERT INTO sdgds_audit_events
                       (actor_id,action,resource_type,resource_id,outcome,correlation_id)
                       VALUES ('synthetic-actor','term.propose','term','HSMART-0099','success','corr-1')"""
                )
                conn.execute(
                    """INSERT INTO sdgds_outbox_events
                       (aggregate_type,aggregate_id,event_type,payload,idempotency_key)
                       VALUES ('term','HSMART-0099','term.proposed','{"term_id":"HSMART-0099"}','idem-rollback')"""
                )
                raise RuntimeError("synthetic forced rollback")
        assert conn.execute("SELECT count(*) FROM sdgds_terms WHERE term_id='HSMART-0099'").fetchone()[0] == 0
        assert conn.execute("SELECT count(*) FROM sdgds_audit_events WHERE resource_id='HSMART-0099'").fetchone()[0] == 0
        assert conn.execute("SELECT count(*) FROM sdgds_outbox_events WHERE idempotency_key='idem-rollback'").fetchone()[0] == 0

        with conn.transaction():
            insert_term(conn, "HSMART-0100", "Committed", "committed")
            conn.execute(
                """INSERT INTO sdgds_audit_events
                   (actor_id,action,resource_type,resource_id,outcome,correlation_id)
                   VALUES ('synthetic-actor','term.propose','term','HSMART-0100','success','corr-2')"""
            )
            conn.execute(
                """INSERT INTO sdgds_outbox_events
                   (aggregate_type,aggregate_id,event_type,payload,idempotency_key)
                   VALUES ('term','HSMART-0100','term.proposed','{"term_id":"HSMART-0100"}','idem-commit')"""
            )
        assert conn.execute("SELECT count(*) FROM sdgds_terms WHERE term_id='HSMART-0100'").fetchone()[0] == 1
        assert conn.execute("SELECT count(*) FROM sdgds_audit_events WHERE resource_id='HSMART-0100'").fetchone()[0] == 1
        assert conn.execute("SELECT count(*) FROM sdgds_outbox_events WHERE idempotency_key='idem-commit'").fetchone()[0] == 1
