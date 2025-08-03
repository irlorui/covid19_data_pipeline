{{
    config(enabled=true)
}}

WITH all_interventions AS (
    SELECT 
        trim(unnest(string_to_array(interventions, '|'))) AS source_intervention
    FROM {{ source('raw', 'covid_clinical_trials') }}
    WHERE interventions IS NOT NULL
)
SELECT
    {{ str_to_int("split_part(source_intervention, ':', 1)") }} AS intervention_id,
    split_part(source_intervention, ':', 1) AS intervention_name
FROM all_interventions
GROUP BY 2
