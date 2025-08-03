{{
    config(enabled=true)
}}


SELECT
    {{ str_to_int("condition") }} AS condition_id,
    condition AS condition_name
FROM {{ ref('lst_conditions') }}
GROUP BY 2
ORDER BY 2
