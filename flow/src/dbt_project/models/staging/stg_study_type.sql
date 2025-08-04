{{
    config(enabled=true)
}}


SELECT 
    {{ str_to_int("study_type") }} AS study_type_id,
    study_type AS study_type_name
FROM {{ source('raw', 'covid_clinical_trials') }}
WHERE study_type IS NOT NULL
GROUP BY study_type
ORDER BY 1