{{
    config(enabled=true)
}}


SELECT *
FROM {{ ref('stg_phase') }}
