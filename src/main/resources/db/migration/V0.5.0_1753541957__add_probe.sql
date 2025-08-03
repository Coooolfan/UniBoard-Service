-- 创建与探针相关的表服务
-- 预计发布于0.5.0版本

CREATE TABLE public.probe_target
(
    id               BIGSERIAL PRIMARY KEY,
    name             TEXT             NOT NULL,
    description      TEXT             NOT NULL,
    key              TEXT             NOT NULL,
    latitude         DOUBLE PRECISION NOT NULL,
    longitude        DOUBLE PRECISION NOT NULL,
    report_times     TIMESTAMPTZ[]    NOT NULL,
    last_report_data JSONB,
    last_report_time TIMESTAMPTZ      NOT NULL DEFAULT to_timestamp(0),
    UNIQUE (key, name)
);
