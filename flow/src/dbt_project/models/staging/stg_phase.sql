{{
    config(enabled=true)
}}


SELECT 
    {{ str_to_int("phases") }} AS phase_id,
    phases AS phase_name
FROM {{ source('raw', 'covid_clinical_trials') }}
WHERE phases IS NOT NULL
GROUP BY phases
ORDER BY SUBSTRING(phases FROM '\d+')