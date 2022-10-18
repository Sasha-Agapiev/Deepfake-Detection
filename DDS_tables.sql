--Tables

CREATE TABLE IF NOT EXISTS "DDSystem"."Contains"
(
    picture "char" NOT NULL,
    prediction real,
    website "char" NOT NULL,
    CONSTRAINT "Contains_pkey" PRIMARY KEY (website, picture),
    CONSTRAINT "Contains_website_fkey" FOREIGN KEY (website)
        REFERENCES "DDSystem"."Website" (url) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "DDSystem"."Contains"
    OWNER to postgres;


CREATE TABLE IF NOT EXISTS "DDSystem"."Receipt"
(
    uid integer NOT NULL,
    total real NOT NULL,
    date date NOT NULL,
    receipt_no "char",
    invoice_no "char" NOT NULL,
    CONSTRAINT "Receipt_pkey" PRIMARY KEY (invoice_no),
    CONSTRAINT "Receipt_uid_fkey" FOREIGN KEY (uid)
        REFERENCES "DDSystem"."User" (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "DDSystem"."Receipt"
    OWNER to postgres;


CREATE TABLE IF NOT EXISTS "DDSystem"."Reports"
(
    uid integer NOT NULL,
    datereported date NOT NULL,
    website "char" NOT NULL,
    add_remove boolean,
    CONSTRAINT "Reports_pkey" PRIMARY KEY (website, uid),
    CONSTRAINT "Reports_uid_fkey" FOREIGN KEY (uid)
        REFERENCES "DDSystem"."User" (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "Reports_website_fkey" FOREIGN KEY (website)
        REFERENCES "DDSystem"."Website" (url) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "DDSystem"."Reports"
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS "DDSystem"."User"
(
    uid integer NOT NULL,
    firstname "char" NOT NULL,
    lastname "char" NOT NULL,
    email "char" NOT NULL,
    password "char" NOT NULL,
    city "char" NOT NULL,
    state "char" NOT NULL,
    zip "char" NOT NULL,
    subscribed boolean NOT NULL,
    CONSTRAINT "User_pkey" PRIMARY KEY (uid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "DDSystem"."User"
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS "DDSystem"."Website"
(
    url "char" NOT NULL,
    domainname "char" NOT NULL,
    flagged boolean DEFAULT false,
    CONSTRAINT "Website_pkey" PRIMARY KEY (url)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "DDSystem"."Website"
    OWNER to postgres;



