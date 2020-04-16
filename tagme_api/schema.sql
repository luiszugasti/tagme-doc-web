DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS document_entity;

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE users (
        id INTEGER NOT NULL,
        first_name VARCHAR,
        last_name VARCHAR,
        email VARCHAR,
        password VARCHAR,
        PRIMARY KEY (id),
        UNIQUE (email)
);

CREATE TABLE document_entity (
        document_name VARCHAR(100),
        entity_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL
);

INSERT INTO "users" VALUES(1,'John','Hamshrit','gmail@gmail.com','superclever123');
COMMIT;