-- PostgreSQL 16 target DDL.
-- Canonical HSMART term IDs are strings (e.g. HSMART-0001), not UUIDs.
-- This migration is additive and intentionally contains no DROP statements.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS sdgds_terms (
    term_id TEXT PRIMARY KEY CHECK (length(term_id) BETWEEN 3 AND 128),
    canonical_label TEXT NOT NULL,
    slug TEXT NOT NULL,
    aliases JSONB NOT NULL DEFAULT '[]'::jsonb CHECK (jsonb_typeof(aliases) = 'array'),
    definition TEXT NOT NULL CHECK (length(trim(definition)) > 0),
    status TEXT NOT NULL CHECK (status IN ('Proposed','Needs Review','Canonical','Deprecated','Historical')),
    domains JSONB NOT NULL DEFAULT '[]'::jsonb CHECK (jsonb_typeof(domains) = 'array'),
    provenance JSONB NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(provenance) = 'object'),
    version INTEGER NOT NULL DEFAULT 1 CHECK (version > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_sdgds_terms_label_ci ON sdgds_terms (lower(canonical_label));
CREATE UNIQUE INDEX IF NOT EXISTS uq_sdgds_terms_slug_ci ON sdgds_terms (lower(slug));
CREATE INDEX IF NOT EXISTS ix_sdgds_terms_status ON sdgds_terms (status);

CREATE TABLE IF NOT EXISTS sdgds_term_aliases (
    alias_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    term_id TEXT NOT NULL REFERENCES sdgds_terms(term_id) ON DELETE RESTRICT,
    alias TEXT NOT NULL CHECK (length(trim(alias)) > 0),
    language TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_sdgds_alias_per_term UNIQUE (term_id, alias)
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_sdgds_alias_ci ON sdgds_term_aliases (lower(alias));

CREATE TABLE IF NOT EXISTS sdgds_term_relations (
    relation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_term_id TEXT NOT NULL REFERENCES sdgds_terms(term_id) ON DELETE RESTRICT,
    target_term_id TEXT NOT NULL REFERENCES sdgds_terms(term_id) ON DELETE RESTRICT,
    relation_type TEXT NOT NULL CHECK (relation_type IN ('synonym','alias','parent','child','depends_on','contrasts_with','replaces')),
    provenance JSONB NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(provenance) = 'object'),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_sdgds_no_self_relation CHECK (source_term_id <> target_term_id),
    CONSTRAINT uq_sdgds_relation UNIQUE (source_term_id, target_term_id, relation_type)
);

CREATE TABLE IF NOT EXISTS sdgds_audit_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id TEXT NOT NULL,
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    outcome TEXT NOT NULL,
    correlation_id TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb CHECK (jsonb_typeof(metadata) = 'object'),
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sdgds_outbox_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type TEXT NOT NULL,
    aggregate_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload JSONB NOT NULL CHECK (jsonb_typeof(payload) = 'object'),
    idempotency_key TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    published_at TIMESTAMPTZ,
    attempts INTEGER NOT NULL DEFAULT 0 CHECK (attempts >= 0)
);
CREATE INDEX IF NOT EXISTS ix_sdgds_outbox_pending ON sdgds_outbox_events (created_at) WHERE published_at IS NULL;
