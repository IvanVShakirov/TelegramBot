create table if not exists users
(
    chat_id   bigint            not null
        constraint users_pk
            primary key,
    username  text,
    full_name text,
    id        serial            not null
);

alter table users
    owner to postgres;

create unique index if not exists users_id_uindex
    on users (id);

create table if not exists document
(
    id        serial            not null
        constraint documetn_pk
            primary key,
    document_text   text,
    document_creator  text,
    document_answer text
);

alter table document
    owner to postgres;

create unique index if not exists document_id_uindex
    on document (id);