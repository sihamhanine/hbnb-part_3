-- initial sql script to create postgreSQL database

-- Create the database
DROP DATABASE IF EXISTS production;
CREATE DATABASE production;

-- Check if the hbnb user exists and create it if not
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'admin') THEN

      CREATE USER hbnb WITH PASSWORD 'hbnb_pwd';
   END IF;
END
$do$;

-- Grant privileges to the hbnb user
GRANT ALL PRIVILEGES ON DATABASE production TO hbnb;
