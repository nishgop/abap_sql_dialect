-- ============================================================================
-- EXTENDED ABAP SQL Example Queries - Comprehensive SQL Variant Coverage
-- ============================================================================

-- ============================================================================
-- 1. JOIN VARIANTS
-- ============================================================================

-- INNER JOIN
SELECT f.carrid, f.connid, p.cityfrom, p.cityto
FROM sflight AS f
INNER JOIN spfli AS p ON f.carrid = p.carrid AND f.connid = p.connid;

-- LEFT OUTER JOIN
SELECT c.name, c.city, b.fldate
FROM scustom AS c
LEFT OUTER JOIN sbook AS b ON c.id = b.customid;

-- RIGHT OUTER JOIN
SELECT c.name, b.carrid, b.fldate
FROM scustom AS c
RIGHT OUTER JOIN sbook AS b ON c.id = b.customid;

-- FULL OUTER JOIN
SELECT c.name, b.carrid
FROM scustom AS c
FULL OUTER JOIN sbook AS b ON c.id = b.customid;

-- CROSS JOIN
SELECT c.name, s.carrid
FROM scustom AS c
CROSS JOIN scarr AS s;

-- Multiple JOINs
SELECT f.carrid, f.connid, p.cityfrom, c.name
FROM sflight AS f
INNER JOIN spfli AS p ON f.carrid = p.carrid
LEFT JOIN sbook AS b ON f.carrid = b.carrid
LEFT JOIN scustom AS c ON b.customid = c.id;

-- Self JOIN
SELECT e1.name as employee, e2.name as manager
FROM employees AS e1
LEFT JOIN employees AS e2 ON e1.manager_id = e2.id;

-- ============================================================================
-- 2. AGGREGATE FUNCTIONS
-- ============================================================================

-- COUNT
SELECT carrid, COUNT(*) as flight_count
FROM sflight
GROUP BY carrid;

-- COUNT DISTINCT
SELECT COUNT(DISTINCT carrid) as unique_carriers
FROM sflight;

-- SUM
SELECT carrid, SUM(seatsocc) as total_seats
FROM sflight
GROUP BY carrid;

-- AVG
SELECT carrid, AVG(seatsocc) as avg_seats
FROM sflight
GROUP BY carrid;

-- MIN and MAX
SELECT carrid,
       MIN(seatsocc) as min_seats,
       MAX(seatsocc) as max_seats
FROM sflight
GROUP BY carrid;

-- Multiple aggregates
SELECT carrid,
       COUNT(*) as flight_count,
       SUM(seatsocc) as total_seats,
       AVG(seatsocc) as avg_seats,
       MIN(seatsocc) as min_seats,
       MAX(seatsocc) as max_seats
FROM sflight
GROUP BY carrid;

-- GROUP BY multiple columns
SELECT carrid, connid, COUNT(*) as flight_count
FROM sflight
GROUP BY carrid, connid;

-- HAVING with aggregates
SELECT carrid, AVG(seatsocc) as avg_seats
FROM sflight
GROUP BY carrid
HAVING AVG(seatsocc) > 100 AND COUNT(*) > 5;

-- ============================================================================
-- 3. WINDOW FUNCTIONS (PARTITIONS)
-- ============================================================================

-- ROW_NUMBER
SELECT carrid, connid, fldate,
       ROW_NUMBER() OVER (ORDER BY fldate) as row_num
FROM sflight;

-- ROW_NUMBER with PARTITION BY
SELECT carrid, connid, fldate,
       ROW_NUMBER() OVER (PARTITION BY carrid ORDER BY fldate) as row_num
FROM sflight;

-- RANK
SELECT carrid, seatsocc,
       RANK() OVER (ORDER BY seatsocc DESC) as rank
FROM sflight;

-- DENSE_RANK
SELECT carrid, seatsocc,
       DENSE_RANK() OVER (ORDER BY seatsocc DESC) as dense_rank
FROM sflight;

-- LAG
SELECT carrid, fldate, seatsocc,
       LAG(seatsocc, 1) OVER (PARTITION BY carrid ORDER BY fldate) as prev_seats
FROM sflight;

-- LEAD
SELECT carrid, fldate, seatsocc,
       LEAD(seatsocc, 1) OVER (PARTITION BY carrid ORDER BY fldate) as next_seats
FROM sflight;

-- SUM OVER
SELECT carrid, seatsocc,
       SUM(seatsocc) OVER (PARTITION BY carrid) as total_by_carrier
FROM sflight;

-- AVG OVER
SELECT carrid, seatsocc,
       AVG(seatsocc) OVER (PARTITION BY carrid) as avg_by_carrier
FROM sflight;

-- FIRST_VALUE
SELECT carrid, fldate, seatsocc,
       FIRST_VALUE(seatsocc) OVER (PARTITION BY carrid ORDER BY fldate) as first_seats
FROM sflight;

-- LAST_VALUE
SELECT carrid, fldate, seatsocc,
       LAST_VALUE(seatsocc) OVER (PARTITION BY carrid ORDER BY fldate
                                  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_seats
FROM sflight;

-- ============================================================================
-- 4. DATE AND TIME FUNCTIONS
-- ============================================================================

-- CURRENT_DATE
SELECT carrid, CURRENT_DATE as today
FROM sflight;

-- CURRENT_TIMESTAMP
SELECT carrid, CURRENT_TIMESTAMP as now
FROM sflight;

-- DATE_TRUNC
SELECT DATE_TRUNC('month', fldate) as month, COUNT(*) as flight_count
FROM sflight
GROUP BY DATE_TRUNC('month', fldate);

-- EXTRACT
SELECT EXTRACT(YEAR FROM fldate) as year,
       EXTRACT(MONTH FROM fldate) as month,
       COUNT(*) as flight_count
FROM sflight
GROUP BY EXTRACT(YEAR FROM fldate), EXTRACT(MONTH FROM fldate);

-- Date arithmetic
SELECT carrid, fldate,
       fldate + INTERVAL '7 days' as next_week,
       fldate - INTERVAL '30 days' as prev_month
FROM sflight;

-- Date difference
SELECT carrid, fldate,
       fldate - CURRENT_DATE as days_until_flight
FROM sflight;

-- ============================================================================
-- 5. STRING FUNCTIONS
-- ============================================================================

-- CONCAT
SELECT CONCAT(carrid, '-', connid) as route_id
FROM sflight;

-- Concatenation with ||
SELECT carrid || '-' || connid as route_id
FROM sflight;

-- SUBSTRING
SELECT carrid, SUBSTRING(carrid, 1, 2) as carrier_prefix
FROM sflight;

-- UPPER
SELECT carrid, UPPER(carrid) as carrier_upper
FROM sflight;

-- LOWER
SELECT carrid, LOWER(carrid) as carrier_lower
FROM sflight;

-- TRIM
SELECT carrid, TRIM(carrid) as carrier_trimmed
FROM sflight;

-- LENGTH
SELECT carrid, LENGTH(carrid) as carrier_length
FROM sflight;

-- REPLACE
SELECT carrid, REPLACE(carrid, 'A', 'X') as modified_carrier
FROM sflight;

-- ============================================================================
-- 6. MATHEMATICAL FUNCTIONS
-- ============================================================================

-- ROUND
SELECT carrid, AVG(seatsocc) as avg_seats,
       ROUND(AVG(seatsocc), 2) as avg_seats_rounded
FROM sflight
GROUP BY carrid;

-- CEIL
SELECT seatsocc, CEIL(seatsocc / 10.0) as ceiling_val
FROM sflight;

-- FLOOR
SELECT seatsocc, FLOOR(seatsocc / 10.0) as floor_val
FROM sflight;

-- ABS
SELECT carrid, seatsocc,
       ABS(seatsocc - 200) as difference_from_200
FROM sflight;

-- MOD
SELECT carrid, seatsocc,
       MOD(seatsocc, 10) as remainder
FROM sflight;

-- POWER
SELECT seatsocc, POWER(seatsocc, 2) as seats_squared
FROM sflight;

-- SQRT
SELECT seatsocc, SQRT(seatsocc) as seats_sqrt
FROM sflight;

-- ============================================================================
-- 7. ORDER BY VARIANTS
-- ============================================================================

-- ORDER BY single column
SELECT carrid, connid FROM sflight ORDER BY carrid;

-- ORDER BY ASC/DESC
SELECT carrid, connid FROM sflight ORDER BY carrid ASC, connid DESC;

-- ORDER BY expression
SELECT carrid, seatsocc FROM sflight ORDER BY seatsocc * 2 DESC;

-- ORDER BY CASE
SELECT carrid, seatsocc
FROM sflight
ORDER BY CASE
           WHEN seatsocc > 200 THEN 1
           WHEN seatsocc > 100 THEN 2
           ELSE 3
         END;

-- ORDER BY with NULLS FIRST/LAST
SELECT carrid, seatsocc FROM sflight ORDER BY seatsocc NULLS FIRST;
SELECT carrid, seatsocc FROM sflight ORDER BY seatsocc NULLS LAST;

-- ============================================================================
-- 8. SET OPERATIONS
-- ============================================================================

-- UNION
SELECT carrid FROM sflight WHERE carrid = 'AA'
UNION
SELECT carrid FROM sflight WHERE carrid = 'LH';

-- UNION ALL
SELECT carrid FROM sflight WHERE carrid = 'AA'
UNION ALL
SELECT carrid FROM sflight WHERE carrid = 'LH';

-- INTERSECT
SELECT carrid FROM sflight
INTERSECT
SELECT carrid FROM spfli;

-- EXCEPT (or MINUS)
SELECT carrid FROM sflight
EXCEPT
SELECT carrid FROM spfli;

-- ============================================================================
-- 9. COMMON TABLE EXPRESSIONS (CTEs)
-- ============================================================================

-- Simple CTE
WITH carrier_stats AS (
  SELECT carrid, COUNT(*) as flight_count
  FROM sflight
  GROUP BY carrid
)
SELECT * FROM carrier_stats WHERE flight_count > 10;

-- Multiple CTEs
WITH carrier_stats AS (
  SELECT carrid, COUNT(*) as flight_count FROM sflight GROUP BY carrid
),
route_stats AS (
  SELECT carrid, connid, AVG(seatsocc) as avg_seats FROM sflight GROUP BY carrid, connid
)
SELECT c.carrid, c.flight_count, r.avg_seats
FROM carrier_stats c
JOIN route_stats r ON c.carrid = r.carrid;

-- ============================================================================
-- 10. SUBQUERIES
-- ============================================================================

-- Scalar subquery
SELECT carrid, seatsocc,
       (SELECT AVG(seatsocc) FROM sflight) as overall_avg
FROM sflight;

-- Subquery in FROM
SELECT *
FROM (
  SELECT carrid, COUNT(*) as cnt FROM sflight GROUP BY carrid
) AS carrier_stats
WHERE cnt > 10;

-- Correlated subquery
SELECT carrid, seatsocc
FROM sflight f1
WHERE seatsocc > (SELECT AVG(seatsocc) FROM sflight f2 WHERE f2.carrid = f1.carrid);

-- EXISTS subquery
SELECT carrid
FROM spfli p
WHERE EXISTS (SELECT 1 FROM sflight f WHERE f.carrid = p.carrid);

-- NOT EXISTS subquery
SELECT carrid
FROM spfli p
WHERE NOT EXISTS (SELECT 1 FROM sflight f WHERE f.carrid = p.carrid);

-- IN subquery
SELECT carrid, connid
FROM spfli
WHERE carrid IN (SELECT DISTINCT carrid FROM sflight WHERE seatsocc > 250);

-- ============================================================================
-- 11. COMPLEX REAL-WORLD EXAMPLES
-- ============================================================================

-- Find top 5 routes by average occupancy
SELECT carrid, connid,
       AVG(seatsocc) as avg_seats,
       COUNT(*) as flight_count
FROM sflight
GROUP BY carrid, connid
HAVING COUNT(*) >= 5
ORDER BY avg_seats DESC
LIMIT 5;

-- Calculate running total with window function
SELECT carrid, fldate, seatsocc,
       SUM(seatsocc) OVER (PARTITION BY carrid ORDER BY fldate
                           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
FROM sflight;

-- Year-over-year comparison
WITH yearly_stats AS (
  SELECT EXTRACT(YEAR FROM fldate) as year,
         carrid,
         SUM(seatsocc) as total_seats
  FROM sflight
  GROUP BY EXTRACT(YEAR FROM fldate), carrid
)
SELECT year, carrid, total_seats,
       LAG(total_seats, 1) OVER (PARTITION BY carrid ORDER BY year) as prev_year_seats,
       total_seats - LAG(total_seats, 1) OVER (PARTITION BY carrid ORDER BY year) as yoy_change
FROM yearly_stats;

-- Percentile calculation
SELECT carrid,
       seatsocc,
       PERCENT_RANK() OVER (PARTITION BY carrid ORDER BY seatsocc) as percentile_rank
FROM sflight;

-- Moving average
SELECT carrid, fldate, seatsocc,
       AVG(seatsocc) OVER (PARTITION BY carrid ORDER BY fldate
                           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg_3
FROM sflight;

