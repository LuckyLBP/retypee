-- Reviews for the tool pages: a star rating and an optional name. New rows start as 'pending' and only show once approved.
create table if not exists reviews (
  id          bigserial primary key,
  tool        text        not null check (tool ~ '^[a-z0-9-]{1,40}$'),
  stars       smallint    not null check (stars between 1 and 5),
  name        text        check (name is null or char_length(name) <= 40),
  lang        text        not null default 'sv' check (lang in ('sv', 'en')),
  status      text        not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  created_at  timestamptz not null default now()
);
create index if not exists reviews_tool_status_idx on reviews (tool, status, created_at desc);
