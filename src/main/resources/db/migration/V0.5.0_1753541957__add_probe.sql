-- 创建与探针相关的表服务
-- 预计发布于0.5.0版本

CREATE TABLE public.probe_target
(
    id          BIGSERIAL PRIMARY KEY,
    name        TEXT             NOT NULL,
    description TEXT             NOT NULL,
    key         TEXT             NOT NULL,
    latitude    DOUBLE PRECISION NOT NULL,
    longitude   DOUBLE PRECISION NOT NULL
);

CREATE TABLE public.probe_metric
(
    id              BIGSERIAL PRIMARY KEY,
    name            TEXT             NOT NULL,
    unit            TEXT             NOT NULL,
    min             DOUBLE PRECISION NOT NULL,
    max             DOUBLE PRECISION NOT NULL,
    probe_target_id BIGINT           NOT NULL REFERENCES public.probe_target (id) ON DELETE CASCADE ON UPDATE CASCADE,

    UNIQUE (name, probe_target_id)
);

CREATE TABLE public.probe_metric_data
(
    id              BIGSERIAL PRIMARY KEY,
    value           DOUBLE PRECISION NOT NULL,
    report_time     TIMESTAMP        NOT NULL,
    probe_metric_id BIGINT           NOT NULL REFERENCES public.probe_metric (id) ON DELETE CASCADE ON UPDATE CASCADE
);