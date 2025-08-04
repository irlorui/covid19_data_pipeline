--Macro to normalize conditions most frequent cases related to COVID19 and SARS-COv-2
{% macro normalize_condition(condition) %}
(CASE WHEN {{condition}} ~* 'covid' THEN 'COVID-19'
      WHEN {{condition}} ~* '(sars.cov.*2)|corona.*virus' THEN 'SARS-CoV-2'
      ELSE {{condition}}::text 
 END)
{% endmacro %}

--Macro to standarize the different formats of dates
{% macro str_to_date(raw_date) %}
(CASE --"Month DD, YYYY"
      WHEN {{raw_date}} ~ '\d{1,2},\s*\d{4}'
            THEN TO_DATE({{raw_date}}, 'FMMonth FMDD, YYYY')
      --"Month YYYY"
      WHEN {{raw_date}} ~ '^[A-Za-z]+ \d{4}$'  
            THEN TO_DATE({{raw_date}}, 'FMMonth YYYY') --assume 1st day
      --"Month YYYY D"
      WHEN {{raw_date}} ~ '^[A-Za-z]+ \d{4} \d{1,2}$'
            THEN TO_DATE({{raw_date}}, 'FMMonth YYYY FMDD')
END)
{% endmacro %}

--Macro to create a INTEGER ID from a string
{% macro str_to_int(text) %}
      abs(('x' || substr(md5({{ text }}), 1, 16))::bit(32)::int)
{% endmacro %}