{{
    config(enabled=true)
}}


SELECT *
FROM {{ ref('stg_study_type') }}
