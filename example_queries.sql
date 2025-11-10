-- ABAP SQL Example Queries for Testing
-- These queries demonstrate various ABAP SQL syntax patterns

-- Basic SELECT
SELECT carrid, connid, fldate
FROM sflight
WHERE carrid = 'AA';

-- SELECT with ORDER BY
SELECT carrid, connid, cityfrom, cityto
FROM spfli
WHERE carrid = 'LH'
ORDER BY connid;

-- SELECT with INNER JOIN
SELECT f.carrid, f.connid, f.fldate, p.cityfrom, p.cityto
FROM sflight AS f
INNER JOIN spfli AS p
  ON f.carrid = p.carrid
  AND f.connid = p.connid
WHERE f.carrid = 'AA';

-- SELECT with LEFT OUTER JOIN
SELECT c.name, b.customid, b.fldate
FROM scustom AS c
LEFT OUTER JOIN sbook AS b
  ON c.id = b.customid
WHERE c.city = 'NEW YORK';

-- SELECT with aggregate functions
SELECT carrid, COUNT(*) as flight_count, AVG(seatsocc) as avg_seats
FROM sflight
GROUP BY carrid
HAVING COUNT(*) > 10;

-- Complex query with multiple clauses
SELECT carrid, connid, AVG(seatsocc) as avg_occupied
FROM sflight
WHERE fldate >= '20230101'
  AND fldate <= '20231231'
GROUP BY carrid, connid
HAVING AVG(seatsocc) > 100
ORDER BY avg_occupied DESC;

-- SELECT with CASE expression
SELECT carrid,
       connid,
       CASE
         WHEN seatsocc > 200 THEN 'HIGH'
         WHEN seatsocc > 100 THEN 'MEDIUM'
         ELSE 'LOW'
       END as occupancy_level
FROM sflight;

-- SELECT with subquery
SELECT carrid, connid
FROM spfli
WHERE carrid IN (
  SELECT DISTINCT carrid
  FROM sflight
  WHERE seatsocc > 250
);

-- SELECT with multiple conditions
SELECT *
FROM sbook
WHERE customid = '00000001'
  AND carrid = 'LH'
  AND (class = 'C' OR class = 'Y');

-- UPDATE statement
UPDATE sflight
SET seatsocc = seatsocc + 10
WHERE carrid = 'AA'
  AND connid = '0017';

-- DELETE statement
DELETE FROM sbook
WHERE fldate < '20200101';

-- INSERT statement
INSERT INTO spfli (carrid, connid, cityfrom, cityto)
VALUES ('XX', '1234', 'BERLIN', 'MUNICH');

