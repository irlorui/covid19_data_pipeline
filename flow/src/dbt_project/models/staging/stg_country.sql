{{
    config(enabled=true)
}}



WITH separated_locations AS (
    SELECT 
        string_to_array(location, ',') AS array_location,
        array_length(string_to_array(location, ','), 1) AS array_len
    FROM (
        SELECT trim(unnest(string_to_array(locations, '|'))) AS location
        FROM {{ source('raw', 'covid_clinical_trials') }}
        WHERE locations IS NOT NULL
    ) sub
),
extracted AS (
    SELECT
        trim(array_location[array_len]) as country -- Country is always the last part
    FROM separated_locations
)
SELECT
    {{ str_to_int("concat(country)") }} as country_id,
    country as country_name
FROM extracted
GROUP BY 2
ORDER BY 2
