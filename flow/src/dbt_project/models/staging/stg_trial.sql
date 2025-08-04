{{
    config(enabled=true)
}}


SELECT 
    {{ str_to_int("nct_number") }} AS trial_id,
    nct_number::TEXT,
    {{ str_to_date("start_date") }} AS started_at,
    {{ str_to_date("primary_completion_date") }} AS primary_completed_at,
    {{ str_to_date("completion_date") }} AS completed_at,
    {{ str_to_date("first_posted") }} AS first_posted_at,
    {{ str_to_date("last_update_posted") }} AS last_update_posted_at,
    interventions::TEXT,
    enrollment::NUMERIC::INT,
    st.study_type_id::INT,
    sp.phase_id,
    acronym::TEXT,
    title::TEXT
FROM {{ source('raw', 'covid_clinical_trials') }} c
LEFT JOIN {{ ref('stg_study_type') }} st
    ON c.study_type = st.study_type_name
LEFT JOIN {{ ref('stg_phase') }} sp
    ON c.phases = sp.phase_name
ORDER BY 2