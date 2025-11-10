-- ============================================================================
-- ENHANCED ABAP SQL SYNTAX EXAMPLES
-- ============================================================================
-- This file contains examples of newly added ABAP SQL features
-- ============================================================================

-- ============================================================================
-- 1. INTO CLAUSES
-- ============================================================================

-- Simple INTO variable
SELECT SINGLE carrid, connid 
FROM sflight 
WHERE carrid = 'AA';

-- INTO with host variable (modern syntax)
SELECT carrid 
FROM sflight 
WHERE carrid = 'AA';

-- INTO TABLE (internal table)
SELECT carrid, connid 
FROM sflight 
WHERE carrid = 'AA';

-- APPENDING TABLE
SELECT carrid, connid 
FROM sflight 
WHERE carrid = 'LH';

-- INTO CORRESPONDING FIELDS OF
SELECT * 
FROM sflight 
WHERE carrid = 'AA';

-- ============================================================================
-- 2. UP TO n ROWS
-- ============================================================================

-- Basic UP TO n ROWS
SELECT * 
FROM sflight 
UP TO 10 ROWS;

-- UP TO with WHERE clause
SELECT carrid, connid 
FROM sflight 
WHERE carrid = 'AA' 
UP TO 100 ROWS;

-- UP TO with ORDER BY
SELECT * 
FROM sflight 
ORDER BY fldate DESC 
UP TO 50 ROWS;

-- ============================================================================
-- 3. BYPASSING BUFFER
-- ============================================================================

-- Basic BYPASSING BUFFER
SELECT * 
FROM sflight 
BYPASSING BUFFER 
WHERE carrid = 'AA';

-- BYPASSING BUFFER with other clauses
SELECT carrid, COUNT(*) as cnt 
FROM sflight 
BYPASSING BUFFER 
GROUP BY carrid;

-- ============================================================================
-- 4. CLIENT SPECIFIED
-- ============================================================================

-- Basic CLIENT SPECIFIED
SELECT * 
FROM t000 
CLIENT SPECIFIED 
WHERE mandt = '100';

-- CLIENT SPECIFIED with conditions
SELECT mandt, bukrs, butxt 
FROM t001 
CLIENT SPECIFIED 
WHERE mandt IN ('100', '200');

-- ============================================================================
-- 5. FOR UPDATE
-- ============================================================================

-- Basic FOR UPDATE
SELECT * 
FROM sflight 
WHERE carrid = 'AA' 
FOR UPDATE;

-- FOR UPDATE with UP TO
SELECT * 
FROM sflight 
WHERE carrid = 'AA' 
UP TO 10 ROWS 
FOR UPDATE;

-- ============================================================================
-- 6. PACKAGE SIZE
-- ============================================================================

-- Basic PACKAGE SIZE
SELECT * 
FROM sflight 
PACKAGE SIZE 1000;

-- PACKAGE SIZE with conditions
SELECT carrid, connid 
FROM sflight 
WHERE carrid IN ('AA', 'LH', 'DL') 
PACKAGE SIZE 500;

-- ============================================================================
-- 7. COMBINED ABAP FEATURES
-- ============================================================================

-- Multiple ABAP keywords together
SELECT carrid, connid, fldate 
FROM sflight 
WHERE carrid = 'AA' 
UP TO 100 ROWS 
BYPASSING BUFFER;

-- Complex query with many ABAP features
SELECT SINGLE carrid, connid, fldate, seatsocc 
FROM sflight 
CLIENT SPECIFIED 
WHERE mandt = '100' 
  AND carrid = 'AA' 
  AND connid = '0017' 
BYPASSING BUFFER 
FOR UPDATE;

-- SELECT with INTO and multiple clauses
SELECT carrid, connid 
FROM sflight 
WHERE carrid = 'AA' 
UP TO 50 ROWS;

-- ============================================================================
-- 8. ABAP STRING FUNCTIONS
-- ============================================================================

-- CONCAT_WITH_SPACE function
SELECT CONCAT_WITH_SPACE(firstname, lastname, 1) as fullname 
FROM employees;

-- STRING_AGG (aggregate function)
SELECT carrid, STRING_AGG(connid, ',') as connections 
FROM spfli 
GROUP BY carrid;

-- CAST function
SELECT CAST(price AS DECIMAL(10,2)) as decimal_price 
FROM products;

-- COALESCE function
SELECT COALESCE(email, phone, 'N/A') as contact 
FROM customers;

-- ============================================================================
-- 9. ABAP HOST VARIABLES
-- ============================================================================

-- Modern host variable syntax (@)
SELECT * 
FROM sflight 
WHERE carrid = @lv_carrid 
  AND connid = @lv_connid;

-- Classic host variable syntax (:)
SELECT * 
FROM sflight 
WHERE carrid = :lv_carrid;

-- Host variables in subquery
SELECT * 
FROM spfli 
WHERE carrid IN (SELECT carrid FROM sflight WHERE connid = @lv_connid);

-- ============================================================================
-- 10. TILDE OPERATOR (~) FOR TABLE ALIASES
-- ============================================================================

-- Tilde in SELECT list
SELECT f~carrid, f~connid, f~fldate 
FROM sflight AS f 
WHERE f~carrid = 'AA';

-- Tilde in JOIN conditions
SELECT f~carrid, f~connid, p~cityfrom, p~cityto 
FROM sflight AS f 
INNER JOIN spfli AS p 
  ON f~carrid = p~carrid 
  AND f~connid = p~connid 
WHERE f~carrid = 'LH';

-- Complex JOIN with tilde
SELECT c~name, b~bookid, f~fldate 
FROM scustom AS c 
INNER JOIN sbook AS b ON c~id = b~customid 
INNER JOIN sflight AS f ON b~carrid = f~carrid AND b~connid = f~connid 
WHERE c~country = 'US';

-- ============================================================================
-- 11. REAL-WORLD ABAP SQL EXAMPLES
-- ============================================================================

-- Flight booking system query
SELECT f~carrid, f~connid, f~fldate, 
       p~cityfrom, p~cityto, 
       f~seatsmax - f~seatsocc as available_seats 
FROM sflight AS f 
INNER JOIN spfli AS p 
  ON f~carrid = p~carrid 
  AND f~connid = p~connid 
WHERE f~fldate > '20230101' 
  AND f~seatsmax - f~seatsocc > 10 
ORDER BY f~fldate 
UP TO 100 ROWS;

-- Customer booking report
SELECT c~name, c~country, COUNT(*) as booking_count, 
       SUM(b~forcuram) as total_amount 
FROM scustom AS c 
INNER JOIN sbook AS b ON c~id = b~customid 
WHERE c~country IN ('US', 'GB', 'DE') 
GROUP BY c~name, c~country 
HAVING COUNT(*) > 5 
ORDER BY total_amount DESC;

-- Data archival query with PACKAGE SIZE
SELECT * 
FROM ztransactions 
WHERE fiscal_year < 2020 
PACKAGE SIZE 10000 
FOR UPDATE;

-- Multi-client query
SELECT mandt, bukrs, butxt, ort01 
FROM t001 
CLIENT SPECIFIED 
WHERE mandt IN ('100', '200', '300') 
ORDER BY mandt, bukrs;

