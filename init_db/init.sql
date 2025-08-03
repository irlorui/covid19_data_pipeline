-------------------------------------------------------------------------------
----------------------------------- SCHEMAS -----------------------------------
-------------------------------------------------------------------------------
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS prod;


-------------------------------------------------------------------------------
-------------------------------------- ROLES ----------------------------------
-------------------------------------------------------------------------------
--DATAOPS ROLE
--In charge of ETLs different steps. Permissions an all schemas
CREATE ROLE dataops;

ALTER SCHEMA raw OWNER TO dataops;
GRANT USAGE, CREATE ON SCHEMA raw to dataops;
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA raw TO dataops;
ALTER DEFAULT PRIVILEGES IN SCHEMA raw 
    GRANT SELECT, INSERT ON TABLES TO dataops;

ALTER SCHEMA staging OWNER TO dataops;
GRANT USAGE, CREATE ON SCHEMA staging to dataops;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA staging TO dataops;
ALTER DEFAULT PRIVILEGES IN SCHEMA staging 
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dataops;

ALTER SCHEMA prod OWNER TO dataops;
GRANT USAGE, CREATE ON SCHEMA prod to dataops;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA prod TO dataops;
ALTER DEFAULT PRIVILEGES IN SCHEMA prod 
    GRANT SELECT, INSERT, UPDATE ON TABLES TO dataops;

--ANALYTICS ROLE
--Can only consume Production data
CREATE ROLE analytics;

GRANT USAGE ON SCHEMA prod to analytics;
GRANT USAGE ON SCHEMA prod to analytics;
GRANT SELECT ON ALL TABLES IN SCHEMA prod TO analytics;
ALTER DEFAULT PRIVILEGES IN SCHEMA prod 
    GRANT SELECT ON TABLES TO analytics;


-------------------------------------------------------------------------------
-------------------------------------- USERS ----------------------------------
-------------------------------------------------------------------------------
CREATE USER etl WITH PASSWORD 'etl';
GRANT dataops TO etl;
GRANT CONNECT ON DATABASE clinical_trials TO etl;

CREATE USER analyst WITH PASSWORD 'analyst';
GRANT analytics TO analyst;
GRANT CONNECT ON DATABASE clinical_trials TO analyst;