ALTER TABLE memes ADD image BLOB;
ALTER TABLE memes ADD image bytea;
-- REQUIRES dropping table on Postgres:
-- DROP TABLE memes;
-- CREATE TABLE memes (id SERIAL, url TEXT, caption1 TEXT, caption2 TEXT, image bytea);
