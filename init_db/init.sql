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

-------------------------------------------------------------------------------
-------------------------------- PRODUCTION TABLES ----------------------------
-------------------------------------------------------------------------------
--Create tables
CREATE TABLE prod.study_type(
    study_type_id INTEGER PRIMARY KEY,
    study_type_name TEXT NOT NULL
);

CREATE TABLE prod.country(
    country_id INTEGER PRIMARY KEY,
    country_name TEXT NOT NULL
);

CREATE TABLE prod.trial_country(
    trial_country_id INTEGER PRIMARY KEY,
    trial_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL
);

CREATE TABLE prod.condition(
    condition_id INTEGER PRIMARY KEY,
    condition_name TEXT NOT NULL
);

CREATE TABLE prod.trial_condition(
    trial_condition_id INTEGER PRIMARY KEY,
    trial_id INTEGER NOT NULL,
    condition_id INTEGER NOT NULL
);

CREATE TABLE prod.intervention(
    intervention_id INTEGER PRIMARY KEY,
    intervention_name TEXT NOT NULL
);

CREATE TABLE prod.trial_intervention(
    trial_intervention_id INTEGER PRIMARY KEY,
    trial_id INTEGER NOT NULL,
    intervention_id INTEGER NOT NULL
);

CREATE TABLE prod.phase(
    phase_id INTEGER PRIMARY KEY,
    phase_name TEXT NOT NULL
);

CREATE TABLE prod.trial(
    trial_id INTEGER PRIMARY KEY,
    nct_number TEXT NOT NULL,
    started_at DATE NULL,
    completed_at DATE NULL,
    primary_completed_at DATE NULL, 
    first_posted_at DATE NULL, 
    last_update_posted_at DATE NULL, 
    enrollment INT NULL,
    study_type_id INT NULL,
    title TEXT NULL,
    acronym TEXT NULL,
    phase_id INT NULL
);


--Add FKs
ALTER TABLE prod.trial ADD CONSTRAINT trial_phase_id_fk 
    FOREIGN KEY (phase_id) REFERENCES prod.phase (phase_id);

ALTER TABLE prod.trial ADD CONSTRAINT trial_study_type_id_fk
    FOREIGN KEY (study_type_id) REFERENCES prod.study_type (study_type_id);

ALTER TABLE prod.trial_country ADD CONSTRAINT trial_country_country_id_fk
    FOREIGN KEY (country_id) REFERENCES prod.country (country_id);

ALTER TABLE prod.trial_country ADD CONSTRAINT trial_country_trial_id_fk
    FOREIGN KEY (trial_id) REFERENCES prod.trial (trial_id);

ALTER TABLE prod.trial_condition ADD CONSTRAINT trial_condition_condition_id_fk
    FOREIGN KEY (condition_id) REFERENCES prod.condition (condition_id);

ALTER TABLE prod.trial_condition ADD CONSTRAINT trial_condition_trial_id_fk
    FOREIGN KEY (trial_id) REFERENCES prod.trial (trial_id);

ALTER TABLE prod.trial_intervention ADD CONSTRAINT trial_intervention_intervention_id_fk
    FOREIGN KEY (intervention_id) REFERENCES prod.intervention (intervention_id);

ALTER TABLE prod.trial_intervention ADD CONSTRAINT trial_intervention_trial_id_fk
    FOREIGN KEY (trial_id) REFERENCES prod.trial (trial_id);
