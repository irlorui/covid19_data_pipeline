{{
    config(enabled=true)
}}



WITH separated_locations AS (
    SELECT 
        nct_number,
        string_to_array(location, ',') AS array_location,
        array_length(string_to_array(location, ','), 1) AS array_len
    FROM (
        SELECT nct_number,
               trim(unnest(string_to_array(locations, '|'))) AS location
        FROM {{ source('raw', 'covid_clinical_trials') }}
        WHERE locations IS NOT NULL
    ) sub
),
extracted_location AS (
    SELECT
        nct_number,
        trim(array_location[array_len]) AS country -- Country is always the last part
    FROM separated_locations
)
SELECT 
    {{ str_to_int("concat(s.trial_id, sl.country_id)") }} as trial_country_id,
    s.trial_id,
    sl.country_id
FROM extracted_location l
INNER JOIN {{ ref('stg_trial') }} s 
    ON s.nct_number = l.nct_number
INNER JOIN {{ ref('stg_country') }} sl
    ON sl.country_name = l.country
GROUP BY 2,3
ORDER BY 2,3
 