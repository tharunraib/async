CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS incidents (
  id UUID PRIMARY KEY,
  external_id TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  component TEXT,
  symptom TEXT,
  dependency TEXT,
  owner TEXT,
  occurred_at TIMESTAMPTZ NOT NULL,
  valid_from TIMESTAMPTZ NOT NULL,
  valid_to TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS chunks (
  id BIGSERIAL PRIMARY KEY,
  incident_id UUID NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  embedding vector(384),
  search_vector tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
);
CREATE INDEX IF NOT EXISTS chunks_fts_idx ON chunks USING gin(search_vector);
CREATE INDEX IF NOT EXISTS chunks_embedding_idx ON chunks USING hnsw (embedding vector_cosine_ops);

CREATE TABLE IF NOT EXISTS recurrence_clusters (
  id UUID PRIMARY KEY,
  label TEXT NOT NULL,
  hypothesis TEXT NOT NULL,
  confidence DOUBLE PRECISION NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS cluster_members (
  cluster_id UUID REFERENCES recurrence_clusters(id) ON DELETE CASCADE,
  incident_id UUID REFERENCES incidents(id) ON DELETE CASCADE,
  PRIMARY KEY(cluster_id, incident_id)
);

CREATE TABLE IF NOT EXISTS remediations (
  id UUID PRIMARY KEY,
  cluster_id UUID REFERENCES recurrence_clusters(id),
  description TEXT NOT NULL,
  expected_outcome TEXT NOT NULL,
  observed_outcome TEXT,
  status TEXT NOT NULL DEFAULT 'pending',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS audit_events (
  id BIGSERIAL PRIMARY KEY,
  event_type TEXT NOT NULL,
  payload JSONB NOT NULL,
  previous_hash TEXT,
  event_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
