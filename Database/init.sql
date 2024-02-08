CREATE ROLE limited_user WITH LOGIN PASSWORD 'password';
GRANT CONNECT ON DATABASE crypto_viz TO limited_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO limited_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO limited_user;

SELECT grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_name='crypto_test' AND grantee='limited_user';