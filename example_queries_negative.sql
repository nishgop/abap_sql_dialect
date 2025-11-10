-- ============================================================================
-- NEGATIVE TEST QUERIES - Invalid ABAP SQL for Error Detection Testing
-- These queries should FAIL validation - used to test error detection
-- ============================================================================

-- ============================================================================
-- 1. SYNTAX ERRORS
-- ============================================================================

-- Missing FROM clause
SELECT carrid, connid WHERE carrid = 'AA';

-- Missing table name
SELECT carrid, connid FROM WHERE carrid = 'AA';

-- Missing SELECT keyword
carrid, connid FROM sflight WHERE carrid = 'AA';

-- Missing WHERE keyword
SELECT carrid, connid FROM sflight carrid = 'AA';

-- Incomplete SELECT
SELECT FROM WHERE;

-- Incomplete JOIN
SELECT f.carrid FROM sflight AS f JOIN;

-- Missing JOIN condition
SELECT f.carrid, p.cityfrom
FROM sflight AS f
INNER JOIN spfli AS p
WHERE f.carrid = 'AA';

-- Invalid JOIN syntax
SELECT * FROM sflight INNER;

-- ============================================================================
-- 2. INVALID COLUMN/TABLE REFERENCES
-- ============================================================================

-- Ambiguous column reference (missing table alias in JOIN)
SELECT carrid, connid
FROM sflight AS f
INNER JOIN spfli AS p ON carrid = carrid;

-- Invalid alias reference
SELECT f.carrid, x.connid
FROM sflight AS f
INNER JOIN spfli AS p ON f.carrid = p.carrid;

-- Missing table alias
SELECT carrid FROM f WHERE carrid = 'AA';

-- ============================================================================
-- 3. AGGREGATE FUNCTION ERRORS
-- ============================================================================

-- Non-aggregated column in GROUP BY query
SELECT carrid, connid, COUNT(*) as cnt
FROM sflight
GROUP BY carrid;

-- Missing GROUP BY for aggregate
SELECT carrid, COUNT(*) as cnt
FROM sflight;

-- Invalid aggregate syntax
SELECT COUNT FROM sflight;

-- Aggregate without parentheses
SELECT COUNT * FROM sflight;

-- ============================================================================
-- 4. INVALID COMPARISON OPERATORS
-- ============================================================================

-- Invalid comparison operator
SELECT carrid FROM sflight WHERE carrid == 'AA';

-- Missing comparison value
SELECT carrid FROM sflight WHERE carrid =;

-- Invalid operator syntax
SELECT carrid FROM sflight WHERE carrid <> =;

-- ============================================================================
-- 5. PARENTHESES ERRORS
-- ============================================================================

-- Unmatched opening parenthesis
SELECT carrid FROM sflight WHERE (carrid = 'AA';

-- Unmatched closing parenthesis
SELECT carrid FROM sflight WHERE carrid = 'AA');

-- Missing opening parenthesis in subquery
SELECT carrid FROM spfli
WHERE carrid IN SELECT carrid FROM sflight);

-- Missing closing parenthesis in function
SELECT COUNT(carrid FROM sflight;

-- ============================================================================
-- 6. STRING LITERAL ERRORS
-- ============================================================================

-- Unclosed string literal
SELECT carrid FROM sflight WHERE carrid = 'AA;

-- Unclosed string with double quotes
SELECT carrid FROM sflight WHERE carrid = "AA;

-- Empty comparison
SELECT carrid FROM sflight WHERE carrid = '';

-- ============================================================================
-- 7. INVALID ORDER BY
-- ============================================================================

-- ORDER BY non-selected column in DISTINCT
SELECT DISTINCT carrid FROM sflight ORDER BY connid;

-- Invalid ORDER BY syntax
SELECT carrid FROM sflight ORDER;

-- Missing column in ORDER BY
SELECT carrid FROM sflight ORDER BY;

-- ============================================================================
-- 8. INVALID HAVING CLAUSE
-- ============================================================================

-- HAVING without GROUP BY
SELECT carrid, COUNT(*) as cnt
FROM sflight
HAVING COUNT(*) > 10;

-- Invalid HAVING syntax
SELECT carrid, COUNT(*) as cnt
FROM sflight
GROUP BY carrid
HAVING;

-- Non-aggregate in HAVING without GROUP BY column
SELECT carrid, COUNT(*) as cnt
FROM sflight
GROUP BY carrid
HAVING connid > 100;

-- ============================================================================
-- 9. INVALID SUBQUERIES
-- ============================================================================

-- Unclosed subquery
SELECT carrid FROM spfli
WHERE carrid IN (SELECT carrid FROM sflight;

-- Subquery in wrong position
SELECT (SELECT carrid) FROM sflight;

-- Multiple columns in scalar subquery
SELECT carrid,
       (SELECT carrid, connid FROM sflight WHERE carrid = 'AA') as sub
FROM spfli;

-- ============================================================================
-- 10. INVALID CASE EXPRESSIONS
-- ============================================================================

-- CASE without END
SELECT carrid,
       CASE
         WHEN seatsocc > 200 THEN 'HIGH'
       as level
FROM sflight;

-- CASE with missing WHEN
SELECT carrid,
       CASE
         seatsocc > 200 THEN 'HIGH'
       END as level
FROM sflight;

-- CASE with missing THEN
SELECT carrid,
       CASE
         WHEN seatsocc > 200 'HIGH'
       END as level
FROM sflight;

-- ============================================================================
-- 11. INVALID SET OPERATIONS
-- ============================================================================

-- UNION with different column counts
SELECT carrid FROM sflight
UNION
SELECT carrid, connid FROM spfli;

-- UNION with incompatible types (conceptual)
SELECT carrid FROM sflight
UNION
SELECT COUNT(*) FROM spfli;

-- Incomplete UNION
SELECT carrid FROM sflight
UNION;

-- ============================================================================
-- 12. INVALID LIMIT/OFFSET
-- ============================================================================

-- Negative LIMIT
SELECT carrid FROM sflight LIMIT -10;

-- LIMIT with invalid value
SELECT carrid FROM sflight LIMIT abc;

-- OFFSET without LIMIT (some dialects)
SELECT carrid FROM sflight OFFSET 10;

-- ============================================================================
-- 13. INVALID WINDOW FUNCTIONS
-- ============================================================================

-- Window function without OVER clause
SELECT carrid, ROW_NUMBER() as rn FROM sflight;

-- Invalid PARTITION BY syntax
SELECT carrid, ROW_NUMBER() OVER (PARTITION) as rn FROM sflight;

-- Missing window specification
SELECT carrid, ROW_NUMBER() OVER as rn FROM sflight;

-- ============================================================================
-- 14. ABAP-SPECIFIC ERRORS
-- ============================================================================

-- SELECT SINGLE without proper WHERE (warning, not error)
-- SELECT SINGLE carrid FROM sflight;

-- Invalid SINGLE placement
SELECT carrid SINGLE FROM sflight;

-- SINGLE after columns
SELECT carrid, connid SINGLE FROM sflight WHERE carrid = 'AA';

-- Multiple SINGLE keywords
SELECT SINGLE SINGLE carrid FROM sflight WHERE carrid = 'AA';

-- ============================================================================
-- 15. INVALID NULL OPERATIONS
-- ============================================================================

-- Using = with NULL instead of IS NULL
SELECT carrid FROM sflight WHERE seatsocc = NULL;

-- Using != with NULL
SELECT carrid FROM sflight WHERE seatsocc != NULL;

-- ============================================================================
-- 16. RESERVED KEYWORD MISUSE
-- ============================================================================

-- Using reserved word as alias without quotes
SELECT carrid as select FROM sflight;

-- Using reserved word as table alias
SELECT s.carrid FROM sflight AS select;

-- ============================================================================
-- 17. INVALID INSERT/UPDATE/DELETE
-- ============================================================================

-- INSERT without VALUES
INSERT INTO sflight (carrid, connid);

-- INSERT with column count mismatch
INSERT INTO sflight (carrid) VALUES ('AA', '0017');

-- UPDATE without SET
UPDATE sflight WHERE carrid = 'AA';

-- UPDATE with invalid SET syntax
UPDATE sflight SET WHERE carrid = 'AA';

-- DELETE without FROM
DELETE WHERE carrid = 'AA';

-- DELETE with invalid syntax
DELETE sflight WHERE carrid = 'AA';

-- ============================================================================
-- 18. INVALID EXPRESSIONS
-- ============================================================================

-- Division by zero (runtime error, but valid syntax)
-- SELECT carrid, seatsocc / 0 as invalid FROM sflight;

-- Invalid arithmetic expression
SELECT carrid, + FROM sflight;

-- Missing operand
SELECT carrid, seatsocc + FROM sflight;

-- Invalid operator sequence
SELECT carrid FROM sflight WHERE seatsocc > < 100;

-- ============================================================================
-- 19. INVALID COMMENTS
-- ============================================================================

-- Unclosed multi-line comment (if supported)
/* SELECT carrid FROM sflight

-- ============================================================================
-- 20. COMPLEX INVALID QUERIES
-- ============================================================================

-- Multiple syntax errors
SELECT carrid connid FROM sflight spfli WHERE;

-- Gibberish query
RANDOM INVALID SQL STATEMENT HERE;

-- Numbers as identifiers
SELECT 123 FROM 456 WHERE 789 = 000;

-- Mixed valid and invalid syntax
SELECT carrid, FROM sflight WHERE carrid = INNER JOIN;

-- ============================================================================
-- END OF NEGATIVE TEST QUERIES
-- ============================================================================
-- Total: 60+ intentionally invalid queries for comprehensive error testing
-- Use these to verify the checker correctly identifies and reports errors
-- ============================================================================

