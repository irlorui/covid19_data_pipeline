{{
    config(enabled=true)
}}

WITH trials_conditions AS (
    SELECT nct_number,
        trim(unnest(string_to_array(conditions, '|'))) AS source_condition
    FROM {{ source('raw', 'covid_clinical_trials') }}
    WHERE conditions IS NOT NULL
)
SELECT 
    {{ str_to_int("concat(s.trial_id, c.condition_id)") }} AS trial_condition_id,
    s.trial_id,
    c.condition_id
FROM trials_conditions t
INNER JOIN {{ ref('stg_trial') }} s 
    ON s.nct_number = t.nct_number
INNER JOIN {{ ref('lst_conditions') }} lc
    ON lc.source_condition = t.source_condition
INNER JOIN {{ ref('stg_condition') }} c
    ON lc.condition = c.condition_name
GROUP BY 2,3
ORDER BY 2,3
