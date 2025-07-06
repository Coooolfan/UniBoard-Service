-- 为hyper_link表添加排序字段和是否公开字段
-- 版本：0.4.1

-- 添加是否公开字段（is_public），默认值为true
ALTER TABLE public.hyper_link
    ADD COLUMN is_public BOOLEAN NOT NULL DEFAULT TRUE;

-- 添加排序字段（sort_order），默认值为0，但先允许重复
ALTER TABLE public.hyper_link
    ADD COLUMN sort_order INTEGER NOT NULL DEFAULT 0;

-- 为现有数据设置唯一的排序值（基于id顺序）
UPDATE public.hyper_link
SET sort_order = (SELECT ROW_NUMBER() OVER (ORDER BY id) - 1
                  FROM public.hyper_link h2
                  WHERE h2.id = hyper_link.id);

-- 添加唯一约束防止sort_order重复
ALTER TABLE public.hyper_link
    ADD CONSTRAINT hyper_link_sort_order_unique UNIQUE (sort_order);
