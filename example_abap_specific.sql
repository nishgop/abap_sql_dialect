-- ============================================================================
-- ABAP-Specific SQL Examples
-- Features unique to ABAP SQL in SAP systems
-- ============================================================================

-- ============================================================================
-- 1. ABAP-SPECIFIC KEYWORDS
-- ============================================================================

-- SINGLE - Select single record
SELECT SINGLE carrid, connid, fldate
FROM sflight
WHERE carrid = 'AA' AND connid = '0017';

-- UP TO n ROWS - Limit result set
SELECT carrid, connid, fldate
FROM sflight
UP TO 10 ROWS
WHERE carrid = 'AA';

-- CLIENT SPECIFIED - Bypass automatic client handling
SELECT * FROM mara CLIENT SPECIFIED
WHERE mandt = '100' AND matnr = '000000000000000001';

-- BYPASSING BUFFER - Skip SAP table buffer
SELECT carrid, connid FROM sflight
BYPASSING BUFFER
WHERE carrid = 'AA';

-- FOR UPDATE - Lock records for update
SELECT carrid, connid FROM sflight
WHERE carrid = 'AA'
FOR UPDATE;

-- ============================================================================
-- 2. ABAP HOST VARIABLES (Parameters)
-- ============================================================================

-- Using host variables (parameters) in WHERE clause
-- In ABAP: SELECT ... WHERE carrid = @lv_carrid
-- Standard SQL equivalent with parameters:
SELECT carrid, connid FROM sflight
WHERE carrid = :lv_carrid;

-- Multiple host variables
SELECT carrid, connid, fldate FROM sflight
WHERE carrid = :lv_carrid
  AND connid = :lv_connid
  AND fldate >= :lv_date_from;

-- Host variables in comparisons
SELECT carrid, seatsocc FROM sflight
WHERE seatsocc > :lv_min_seats
  AND seatsocc < :lv_max_seats;

-- ============================================================================
-- 3. ABAP SELECT INTO VARIANTS
-- ============================================================================

-- Note: INTO clauses are ABAP-specific and happen after FROM
-- These examples show the SELECT part that would work with INTO

-- INTO CORRESPONDING FIELDS OF
SELECT carrid, connid, fldate
FROM sflight
WHERE carrid = 'AA';

-- INTO TABLE (for internal tables)
SELECT carrid, connid
FROM sflight
WHERE carrid = 'AA';

-- APPENDING TABLE (append to existing internal table)
SELECT carrid, connid
FROM sflight
WHERE carrid = 'LH';

-- ============================================================================
-- 4. ABAP JOIN SYNTAX
-- ============================================================================

-- ABAP uses tilde (~) notation in addition to dot notation
-- Standard SQL equivalent with aliases
SELECT f.carrid, f.connid, p.cityfrom, p.cityto
FROM sflight AS f
INNER JOIN spfli AS p
  ON f.carrid = p.carrid
  AND f.connid = p.connid;

-- Multiple table join with ABAP-style
SELECT f.carrid, f.connid, f.fldate,
       p.cityfrom, p.cityto,
       c.name, c.city
FROM sflight AS f
INNER JOIN spfli AS p ON f.carrid = p.carrid AND f.connid = p.connid
LEFT OUTER JOIN sbook AS b ON f.carrid = b.carrid AND f.connid = b.connid
LEFT OUTER JOIN scustom AS c ON b.customid = c.id
WHERE f.carrid = 'AA';

-- ============================================================================
-- 5. ABAP AGGREGATE WITH ABAP-STYLE GROUPING
-- ============================================================================

-- COUNT with DISTINCT
SELECT COUNT(DISTINCT carrid) as unique_carriers
FROM sflight;

-- Multiple aggregates in ABAP style
SELECT carrid,
       COUNT(*) as flight_count,
       SUM(seatsocc) as total_seats,
       AVG(seatsocc) as avg_seats,
       MIN(seatsocc) as min_seats,
       MAX(seatsocc) as max_seats
FROM sflight
GROUP BY carrid
HAVING COUNT(*) > 5;

-- ============================================================================
-- 6. ABAP CASE EXPRESSIONS
-- ============================================================================

-- Simple CASE (testing a single expression)
SELECT carrid,
       CASE carrid
         WHEN 'AA' THEN 'American Airlines'
         WHEN 'LH' THEN 'Lufthansa'
         WHEN 'UA' THEN 'United Airlines'
         ELSE 'Other Carrier'
       END as carrier_name
FROM sflight;

-- Searched CASE (with conditions)
SELECT carrid, seatsocc,
       CASE
         WHEN seatsocc >= 300 THEN 'Very High'
         WHEN seatsocc >= 200 THEN 'High'
         WHEN seatsocc >= 100 THEN 'Medium'
         WHEN seatsocc >= 50 THEN 'Low'
         ELSE 'Very Low'
       END as occupancy_category
FROM sflight;

-- Nested CASE
SELECT carrid, connid, seatsocc,
       CASE
         WHEN carrid = 'AA' THEN
           CASE
             WHEN seatsocc > 200 THEN 'AA-Premium'
             WHEN seatsocc > 100 THEN 'AA-Standard'
             ELSE 'AA-Economy'
           END
         WHEN carrid = 'LH' THEN
           CASE
             WHEN seatsocc > 250 THEN 'LH-Business'
             ELSE 'LH-Economy'
           END
         ELSE 'Other'
       END as flight_category
FROM sflight;

-- ============================================================================
-- 7. LIMIT AND OFFSET (ABAP TOP/UP TO equivalent)
-- ============================================================================

-- LIMIT (similar to UP TO n ROWS)
SELECT carrid, connid FROM sflight
ORDER BY carrid, connid
LIMIT 10;

-- OFFSET (skip rows)
SELECT carrid, connid FROM sflight
ORDER BY carrid, connid
OFFSET 20;

-- LIMIT with OFFSET (pagination)
SELECT carrid, connid FROM sflight
ORDER BY carrid, connid
LIMIT 10 OFFSET 20;

-- FETCH FIRST n ROWS ONLY (SQL standard)
SELECT carrid, connid FROM sflight
ORDER BY carrid, connid
FETCH FIRST 10 ROWS ONLY;

-- ============================================================================
-- 8. NULL HANDLING IN ABAP SQL
-- ============================================================================

-- IS NULL
SELECT carrid, connid FROM sflight
WHERE seatsocc IS NULL;

-- IS NOT NULL
SELECT carrid, connid FROM sflight
WHERE seatsocc IS NOT NULL;

-- COALESCE (return first non-null value)
SELECT carrid,
       COALESCE(seatsocc, 0) as seats_occupied,
       COALESCE(connid, 'UNKNOWN') as connection
FROM sflight;

-- NULLIF (return NULL if values are equal)
SELECT carrid,
       NULLIF(seatsocc, 0) as seats_if_not_zero
FROM sflight;

-- ============================================================================
-- 9. DISTINCT VARIANTS
-- ============================================================================

-- DISTINCT keyword
SELECT DISTINCT carrid FROM sflight;

-- DISTINCT with multiple columns
SELECT DISTINCT carrid, connid FROM sflight;

-- DISTINCT in aggregate
SELECT COUNT(DISTINCT carrid) as unique_carriers,
       COUNT(DISTINCT connid) as unique_connections
FROM sflight;

-- ============================================================================
-- 10. IN OPERATOR VARIANTS
-- ============================================================================

-- IN with literal list
SELECT carrid, connid FROM sflight
WHERE carrid IN ('AA', 'LH', 'UA', 'DL');

-- IN with subquery
SELECT carrid, connid FROM spfli
WHERE carrid IN (
  SELECT DISTINCT carrid FROM sflight WHERE seatsocc > 250
);

-- NOT IN
SELECT carrid, connid FROM spfli
WHERE carrid NOT IN ('AA', 'LH');

-- IN with host variables (ABAP style would use @lt_carriers)
SELECT carrid, connid FROM sflight
WHERE carrid IN (:lv_carr1, :lv_carr2, :lv_carr3);

-- ============================================================================
-- 11. BETWEEN OPERATOR
-- ============================================================================

-- BETWEEN with numbers
SELECT carrid, seatsocc FROM sflight
WHERE seatsocc BETWEEN 100 AND 200;

-- NOT BETWEEN
SELECT carrid, seatsocc FROM sflight
WHERE seatsocc NOT BETWEEN 100 AND 200;

-- BETWEEN with dates
SELECT carrid, fldate FROM sflight
WHERE fldate BETWEEN '20230101' AND '20231231';

-- BETWEEN with parameters
SELECT carrid, seatsocc FROM sflight
WHERE seatsocc BETWEEN :lv_min_seats AND :lv_max_seats;

-- ============================================================================
-- 12. LIKE OPERATOR (Pattern Matching)
-- ============================================================================

-- LIKE with % wildcard (any characters)
SELECT carrid, connid FROM sflight
WHERE carrid LIKE 'A%';

-- LIKE with _ wildcard (single character)
SELECT carrid, connid FROM sflight
WHERE carrid LIKE 'A_';

-- NOT LIKE
SELECT carrid, connid FROM sflight
WHERE carrid NOT LIKE 'A%';

-- LIKE with multiple patterns
SELECT carrid, connid FROM sflight
WHERE carrid LIKE '%A%'
   OR connid LIKE '00%';

-- ============================================================================
-- 13. COMPLEX ABAP SQL PATTERNS
-- ============================================================================

-- Combine multiple ABAP features
SELECT DISTINCT f.carrid, f.connid,
       COUNT(*) as flight_count,
       AVG(f.seatsocc) as avg_occupancy,
       CASE
         WHEN AVG(f.seatsocc) > 200 THEN 'Popular'
         WHEN AVG(f.seatsocc) > 100 THEN 'Normal'
         ELSE 'Low Demand'
       END as route_category
FROM sflight AS f
WHERE f.carrid IN ('AA', 'LH', 'UA')
  AND f.fldate BETWEEN '20230101' AND '20231231'
  AND f.seatsocc IS NOT NULL
GROUP BY f.carrid, f.connid
HAVING COUNT(*) > 10
ORDER BY avg_occupancy DESC
LIMIT 20;

-- Subquery with ABAP patterns
SELECT carrid, connid, seatsocc
FROM sflight
WHERE seatsocc > (
  SELECT AVG(seatsocc)
  FROM sflight
  WHERE carrid IN ('AA', 'LH')
)
AND fldate BETWEEN '20230101' AND '20231231'
ORDER BY seatsocc DESC;

-- CTE with ABAP-style filters
WITH high_occupancy_routes AS (
  SELECT carrid, connid, AVG(seatsocc) as avg_seats
  FROM sflight
  WHERE fldate >= '20230101'
  GROUP BY carrid, connid
  HAVING AVG(seatsocc) > 150
)
SELECT r.carrid, r.connid, r.avg_seats,
       p.cityfrom, p.cityto
FROM high_occupancy_routes r
INNER JOIN spfli p ON r.carrid = p.carrid AND r.connid = p.connid
WHERE r.carrid LIKE 'A%'
ORDER BY r.avg_seats DESC;

