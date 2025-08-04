{{
    config(enabled=true)
}}

WITH all_conditionas AS (
    SELECT 
        trim(unnest(string_to_array(conditions, '|'))) AS source_condition
    FROM {{ source('raw', 'covid_clinical_trials') }}
    WHERE conditions IS NOT NULL
)
SELECT
    source_condition,
    {{ normalize_condition("source_condition") }} AS condition
FROM all_conditionas
GROUP BY source_condition
