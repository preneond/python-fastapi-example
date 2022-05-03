BEGIN;
    DROP TABLE IF EXISTS "users";
    CREATE TABLE users  (
        email VARCHAR NOT NULL PRIMARY KEY ,
        value VARCHAR
    );
COMMIT;
