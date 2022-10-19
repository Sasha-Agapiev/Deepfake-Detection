-- Procedures

CREATE OR REPLACE PROCEDURE "DDSystem".add_contains(
	IN pic "char",
	IN pred real,
	IN url "char")
LANGUAGE 'sql'
AS $BODY$
Insert Into "DDSystem"."Contains" Values (pic, pred, url)
$BODY$;
ALTER PROCEDURE "DDSystem".add_contains("char", real, "char")
    OWNER TO postgres;

CREATE OR REPLACE PROCEDURE "DDSystem".add_reports(
	IN uid integer,
	IN url "char",
	IN a_r boolean)
LANGUAGE 'sql'
AS $BODY$
Insert Into "DDSystem"."Reports" Values (uid, NOW(), url, a_r)
$BODY$;
ALTER PROCEDURE "DDSystem".add_reports(integer, "char", boolean)
    OWNER TO postgres;

CREATE OR REPLACE PROCEDURE "DDSystem".add_user(
	IN uid integer,
	IN firstname "char",
	IN lastname "char",
	IN email "char",
	IN pwd "char",
	IN city "char",
	IN _state "char",
	IN zip "char",
	IN subscribed boolean)
LANGUAGE 'sql'
AS $BODY$
Insert Into "DDSystem"."User" Values (uid, firstname, email, pwd, city, _state, zip, subscribed)
$BODY$;
ALTER PROCEDURE "DDSystem".add_user(integer, "char", "char", "char", "char", "char", "char", "char", boolean)
    OWNER TO postgres;

CREATE OR REPLACE PROCEDURE "DDSystem".add_webstie(
	IN url "char",
	IN domainname "char")
LANGUAGE 'sql'
AS $BODY$
Insert Into "DDSystem"."Website" Values (url, domainname, False)
$BODY$;
ALTER PROCEDURE "DDSystem".add_webstie("char", "char")
    OWNER TO postgres;

CREATE OR REPLACE PROCEDURE "DDSystem".check_reports(
	IN em "char")
LANGUAGE 'sql'
AS $BODY$
Select datereported, website, add_remove
From "DDSystem"."Reports"
Where "DDSystem".uid_from_email(em) = uid
$BODY$;
ALTER PROCEDURE "DDSystem".check_reports("char")
    OWNER TO postgres;

CREATE OR REPLACE PROCEDURE "DDSystem".check_reports(
	IN u integer)
LANGUAGE 'sql'
AS $BODY$
Select datereported, website, add_remove
From "DDSystem"."Reports"
Where u = uid
$BODY$;
ALTER PROCEDURE "DDSystem".check_reports(integer)
    OWNER TO postgres;

CREATE OR REPLACE PROCEDURE "DDSystem".check_subscription(
	IN em "char")
LANGUAGE 'sql'
AS $BODY$
Select subscribed
From "DDSystem"."User"
Where "DDSystem".uid_from_email(em) = uid
$BODY$;
ALTER PROCEDURE "DDSystem".check_subscription("char")
    OWNER TO postgres;

CREATE OR REPLACE PROCEDURE "DDSystem".isflagged(
	IN website "char")
LANGUAGE 'sql'
AS $BODY$
Select flagged 
From "DDSystem"."Website"
Where website = url
$BODY$;
ALTER PROCEDURE "DDSystem".isflagged("char")
    OWNER TO postgres;

CREATE OR REPLACE PROCEDURE "DDSystem".num_remove(
	IN url "char")
LANGUAGE 'sql'
AS $BODY$
Select Count(*) as num_remove
From "DDSystem"."Reports"
Where url = website and add_remove = false
$BODY$;
ALTER PROCEDURE "DDSystem".num_remove("char")
    OWNER TO postgres;

CREATE OR REPLACE PROCEDURE "DDSystem".num_reports(
	IN url "char")
LANGUAGE 'sql'
AS $BODY$
Select Count(*) as num_reports
From "DDSystem"."Reports"
Where url = website And add_remove = true
$BODY$;
ALTER PROCEDURE "DDSystem".num_reports("char")
    OWNER TO postgres;

CREATE OR REPLACE PROCEDURE "DDSystem".update_subscription(
	IN e "char")
LANGUAGE 'sql'
AS $BODY$
Update "DDSystem"."User" Set subscribed = true Where (e = email)
$BODY$;
ALTER PROCEDURE "DDSystem".update_subscription("char")
    OWNER TO postgres;



