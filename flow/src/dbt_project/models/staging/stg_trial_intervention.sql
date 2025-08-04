{{
    config(enabled=true)
}}


WITH all_interventions AS (
    SELECT 
        nct_number,
        trim(unnest(string_to_array(interventions, '|'))) AS source_intervention
    FROM {{ source('raw', 'covid_clinical_trials') }}
    WHERE interventions IS NOT NULL
)
SELECT
    {{ str_to_int("concat(t.trial_id, i.intervention_id)") }} AS trial_intervention_id,
    t.trial_id,
    i.intervention_id
FROM all_interventions ai
INNER JOIN {{ ref('stg_trial') }} t 
    ON ai.nct_number = t.nct_number
INNER JOIN {{ ref('stg_intervention') }} i
    ON split_part(ai.source_intervention, ':', 1) = i.intervention_name
GROUP BY 2,3
ORDER BY 2,3