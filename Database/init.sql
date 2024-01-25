CREATE ROLE limited_user WITH LOGIN PASSWORD 'password';
GRANT CONNECT ON DATABASE crypto_viz TO limited_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO limited_user;