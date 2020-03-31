DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS document;
DROP TABLE IF EXISTS entity;
DROP TABLE IF EXISTS doc_ent_rel;

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

CREATE TABLE document (
        document_id INTEGER NOT NULL,
        document_name VARCHAR(100),
        PRIMARY KEY (document_id),
        UNIQUE (document_name)
);

CREATE TABLE entity (
        entity_id INTEGER NOT NULL,
        entity_title VARCHAR,
        PRIMARY KEY (entity_id),
        UNIQUE (entity_title)
);

CREATE TABLE doc_ent_rel (
        relationship_id INTEGER NOT NULL,
        document_id INTEGER,
        entity_id INTEGER,
        quantity INTEGER NOT NULL,
        PRIMARY KEY (relationship_id),
        CONSTRAINT uk_document_entity_id UNIQUE (document_id, entity_id),
        FOREIGN KEY(document_id) REFERENCES document (document_id),
        FOREIGN KEY(entity_id) REFERENCES entity (entity_id)
);

INSERT INTO "users" VALUES(1,'John','Hamshrit','gmail@gmail.com','superclever123');

INSERT INTO "document" VALUES(1,'test1');
INSERT INTO "document" VALUES(2,'test2');
INSERT INTO "document" VALUES(3,'test3');
INSERT INTO "document" VALUES(4,'test4');
INSERT INTO "document" VALUES(5,'test5');

INSERT INTO "entity" VALUES(1,'Arial');
INSERT INTO "entity" VALUES(2,'Helvetica');
INSERT INTO "entity" VALUES(3,'Sans-serif');
INSERT INTO "entity" VALUES(4,'Height');
INSERT INTO "entity" VALUES(5,'The Da Vinci Code');
INSERT INTO "entity" VALUES(6,'Dan Brown');
INSERT INTO "entity" VALUES(7,'Robert Langdon');
INSERT INTO "entity" VALUES(8,'Ron Howard');
INSERT INTO "entity" VALUES(9,'Film director');
INSERT INTO "entity" VALUES(10,'Brian Grazer');
INSERT INTO "entity" VALUES(11,'John Calley');
INSERT INTO "entity" VALUES(12,'David Koepp');

INSERT INTO "doc_ent_rel" VALUES(1,5,10,6);
INSERT INTO "doc_ent_rel" VALUES(2,1,12,1);
INSERT INTO "doc_ent_rel" VALUES(3,3,10,5);
INSERT INTO "doc_ent_rel" VALUES(4,1,10,4);
INSERT INTO "doc_ent_rel" VALUES(5,1,9,3);
INSERT INTO "doc_ent_rel" VALUES(6,1,8,8);
INSERT INTO "doc_ent_rel" VALUES(7,1,7,7);
INSERT INTO "doc_ent_rel" VALUES(8,4,6,6);
INSERT INTO "doc_ent_rel" VALUES(9,1,5,4);
INSERT INTO "doc_ent_rel" VALUES(10,1,4,3);
INSERT INTO "doc_ent_rel" VALUES(11,5,3,1);
INSERT INTO "doc_ent_rel" VALUES(12,4,2,9);
INSERT INTO "doc_ent_rel" VALUES(13,3,1,8);
INSERT INTO "doc_ent_rel" VALUES(14,2,12,7);
INSERT INTO "doc_ent_rel" VALUES(15,1,11,6);
INSERT INTO "doc_ent_rel" VALUES(16,4,9,5);
INSERT INTO "doc_ent_rel" VALUES(17,3,8,4);
INSERT INTO "doc_ent_rel" VALUES(18,2,7,3);
INSERT INTO "doc_ent_rel" VALUES(19,1,6,6);
INSERT INTO "doc_ent_rel" VALUES(20,5,5,2);
INSERT INTO "doc_ent_rel" VALUES(21,4,4,4);
INSERT INTO "doc_ent_rel" VALUES(22,3,3,8);
INSERT INTO "doc_ent_rel" VALUES(23,2,2,3);
INSERT INTO "doc_ent_rel" VALUES(24,1,1,6);
COMMIT;