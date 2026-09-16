-- checking imported row count
SELECT COUNT(*) AS total_records
FROM properties;

---------------------------------------------
--missing value validation
---------------------------------------------

SELECT
    COUNT(*) FILTER (WHERE longitude IS NULL) AS missing_longitude,
    COUNT(*) FILTER (WHERE latitude IS NULL) AS missing_latitude,
    COUNT(*) FILTER (WHERE housing_median_age IS NULL) AS missing_housing_age,
    COUNT(*) FILTER (WHERE total_rooms IS NULL) AS missing_rooms,
    COUNT(*) FILTER (WHERE total_bedrooms IS NULL) AS missing_bedrooms,
    COUNT(*) FILTER (WHERE population IS NULL) AS missing_population,
    COUNT(*) FILTER (WHERE households IS NULL) AS missing_households,
    COUNT(*) FILTER (WHERE median_income IS NULL) AS missing_income,
    COUNT(*) FILTER (WHERE median_house_value IS NULL) AS missing_house_value,
    COUNT(*) FILTER (WHERE ocean_proximity IS NULL) AS missing_ocean_proximity
FROM properties;

---------------------------------------
-- range summary
---------------------------------------
SELECT
    MIN(median_house_value) AS minimum_value,
    MAX(median_house_value) AS maximum_value,
    ROUND(AVG(median_house_value), 2) AS average_value,
    MIN(median_income) AS minimum_income,
    MAX(median_income) AS maximum_income,
    MIN(housing_median_age) AS newest_housing,
    MAX(housing_median_age) AS oldest_housing
FROM properties;

------------------------------------------
-- capped house value analysis
------------------------------------------
SELECT
    COUNT(*) AS capped_value_rows,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM properties),
        2
    ) AS capped_percentage
FROM properties
WHERE median_house_value = 500001;

----------------------------------------
-- house values by ocean proximity 
----------------------------------------

SELECT
    ocean_proximity,
    COUNT(*) AS total_areas,
    ROUND(AVG(median_house_value), 2) AS average_house_value,
    ROUND(AVG(median_income), 2) AS average_income
FROM properties
GROUP BY ocean_proximity
ORDER BY average_house_value DESC;

---------------------------------------------
-- create calculated property metrics view
---------------------------------------------

CREATE OR REPLACE VIEW property_metrics AS
SELECT
    longitude,
    latitude,
    housing_median_age,
    total_rooms,
    total_bedrooms,
    population,
    households,
    median_income,
    median_house_value,
    ocean_proximity,

    ROUND(
        total_rooms::numeric / NULLIF(households, 0),
        2
    ) AS rooms_per_household,

    ROUND(
        total_bedrooms::numeric / NULLIF(households, 0),
        2
    ) AS bedrooms_per_household,

    ROUND(
        population::numeric / NULLIF(households, 0),
        2
    ) AS people_per_household,

    ROUND(
        total_bedrooms::numeric /
        NULLIF(total_rooms, 0) * 100,
        2
    ) AS bedroom_percentage,

    CASE
        WHEN median_income < 2 THEN 'Low income'
        WHEN median_income < 4 THEN 'Lower-middle income'
        WHEN median_income < 6 THEN 'Upper-middle income'
        ELSE 'High income'
    END AS income_group,

    CASE
        WHEN housing_median_age < 10 THEN 'Under 10 years'
        WHEN housing_median_age < 20 THEN '10–19 years'
        WHEN housing_median_age < 30 THEN '20–29 years'
        WHEN housing_median_age < 40 THEN '30–39 years'
        ELSE '40+ years'
    END AS housing_age_group

FROM properties;

----------------------------------------
-- verifiying property metrics
----------------------------------------

SELECT *
FROM property_metrics
LIMIT 10;

-----------------------------------------
-- finding correlations
------------------------------------------

SELECT
    'All records' AS dataset_group,

    ROUND(
        CORR(median_income, median_house_value)::numeric,
        3
    ) AS income_value_correlation,

    ROUND(
        CORR(rooms_per_household, median_house_value)::numeric,
        3
    ) AS rooms_value_correlation,

    ROUND(
        CORR(people_per_household, median_house_value)::numeric,
        3
    ) AS household_size_value_correlation,

    ROUND(
        CORR(housing_median_age, median_house_value)::numeric,
        3
    ) AS age_value_correlation

FROM property_metrics

UNION ALL

SELECT
    'Excluding capped values' AS dataset_group,

    ROUND(
        CORR(median_income, median_house_value)::numeric,
        3
    ),

    ROUND(
        CORR(rooms_per_household, median_house_value)::numeric,
        3
    ),

    ROUND(
        CORR(people_per_household, median_house_value)::numeric,
        3
    ),

    ROUND(
        CORR(housing_median_age, median_house_value)::numeric,
        3
    )

FROM property_metrics
WHERE median_house_value < 500001;

-------------------------------------
-- house values by income group
-------------------------------------

SELECT
    income_group,
    COUNT(*) AS total_records,

    ROUND(
        AVG(median_income),
        2
    ) AS average_income_score,

    ROUND(
        AVG(median_house_value),
        2
    ) AS average_house_value,

    ROUND(
        PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY median_house_value)::numeric,
        2
    ) AS median_house_value,

    COUNT(*) FILTER (
        WHERE median_house_value = 500001
    ) AS capped_records,

    ROUND(
        COUNT(*) FILTER (
            WHERE median_house_value = 500001
        ) * 100.0 / COUNT(*),
        2
    ) AS capped_percentage

FROM property_metrics
GROUP BY income_group
ORDER BY average_house_value DESC;

----------------------------------------
-- house values by housing age
----------------------------------------
SELECT
    housing_age_group,
    COUNT(*) AS total_records,

    ROUND(
        AVG(housing_median_age),
        2
    ) AS average_age,

    ROUND(
        AVG(median_income),
        2
    ) AS average_income,

    ROUND(
        AVG(median_house_value),
        2
    ) AS average_house_value,

    ROUND(
        PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY median_house_value)::numeric,
        2
    ) AS median_house_value

FROM property_metrics
GROUP BY housing_age_group
ORDER BY average_age;

---------------------------------------
-- location analysis for oldest housing
---------------------------------------
SELECT
    ocean_proximity,
    COUNT(*) AS total_records,

    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_old_housing,

    ROUND(
        AVG(median_income),
        2
    ) AS average_income,

    ROUND(
        AVG(median_house_value),
        2
    ) AS average_house_value

FROM property_metrics
WHERE housing_age_group = '40+ years'
GROUP BY ocean_proximity
ORDER BY total_records DESC;

----------------------------------
