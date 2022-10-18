--Functions

CREATE OR REPLACE FUNCTION "DDSystem".uid_from_email(
	em "char")
    RETURNS integer
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
Select uid
From "DDSystem"."User"
Where em = email
$BODY$;

ALTER FUNCTION "DDSystem".uid_from_email("char")
    OWNER TO postgres;
