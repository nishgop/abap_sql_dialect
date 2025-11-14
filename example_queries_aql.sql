-- ========================================================================
-- AQL (Ariba Query Language) Example Queries
-- Comprehensive collection covering all major AQL features and patterns
-- ========================================================================

-- ========================================================================
-- 1. BASIC SELECT QUERIES
-- ========================================================================

-- Simple SELECT with WHERE clause
SELECT Document.DocumentId, Document.Title, Document.Status
FROM Document
WHERE Document.Status = 'Active';

-- SELECT with multiple conditions
SELECT Document.DocumentId, Document.Amount
FROM Document
WHERE Document.Status = 'Active' AND Document.Amount > 1000;

-- SELECT with OR conditions
SELECT Supplier.SupplierId, Supplier.Name
FROM Supplier
WHERE Supplier.Status = 'Active' OR Supplier.Status = 'Pending';

-- SELECT with IN clause
SELECT Document.DocumentId, Document.Status
FROM Document
WHERE Document.Status IN ('Active', 'Pending', 'Approved');

-- SELECT with BETWEEN
SELECT Invoice.InvoiceId, Invoice.Amount
FROM Invoice
WHERE Invoice.Amount BETWEEN 1000 AND 5000;

-- SELECT with LIKE pattern
SELECT Supplier.Name, Supplier.City
FROM Supplier
WHERE Supplier.Name LIKE '%Corp%';

-- ========================================================================
-- 2. JOIN OPERATIONS
-- ========================================================================

-- INNER JOIN
SELECT d.DocumentId, p.ProjectName, d.Amount
FROM Document d
INNER JOIN Project p ON d.ProjectId = p.ProjectId
WHERE d.Status = 'Active';

-- LEFT OUTER JOIN
SELECT s.SupplierId, s.Name, i.InvoiceId, i.Amount
FROM Supplier s
LEFT OUTER JOIN Invoice i ON s.SupplierId = i.SupplierId;

-- Multiple JOINs
SELECT d.DocumentId, p.ProjectName, s.SupplierName, d.Amount
FROM Document d
INNER JOIN Project p ON d.ProjectId = p.ProjectId
INNER JOIN Supplier s ON d.SupplierId = s.SupplierId
WHERE d.Status = 'Active';

-- JOIN with aggregate
SELECT s.Name, COUNT(i.InvoiceId) as InvoiceCount, SUM(i.Amount) as TotalAmount
FROM Supplier s
LEFT JOIN Invoice i ON s.SupplierId = i.SupplierId
GROUP BY s.Name;

-- ========================================================================
-- 3. AGGREGATE FUNCTIONS
-- ========================================================================

-- COUNT
SELECT COUNT(*) as TotalDocuments
FROM Document
WHERE Document.Status = 'Active';

-- COUNT DISTINCT
SELECT COUNT(DISTINCT Supplier.SupplierId) as UniqueSuppliers
FROM Invoice;

-- SUM
SELECT SUM(Invoice.Amount) as TotalInvoiceAmount
FROM Invoice
WHERE Invoice.Status = 'Paid';

-- AVG
SELECT AVG(Invoice.Amount) as AverageInvoiceAmount
FROM Invoice
WHERE Invoice.Status = 'Paid';

-- MIN and MAX
SELECT MIN(Invoice.Amount) as MinAmount, MAX(Invoice.Amount) as MaxAmount
FROM Invoice;

-- Multiple aggregates
SELECT 
    Document.Status,
    COUNT(*) as Count,
    SUM(Document.Amount) as Total,
    AVG(Document.Amount) as Average,
    MIN(Document.Amount) as Minimum,
    MAX(Document.Amount) as Maximum
FROM Document
GROUP BY Document.Status;

-- ========================================================================
-- 4. GROUP BY and HAVING
-- ========================================================================

-- Simple GROUP BY
SELECT Supplier.Name, COUNT(*) as InvoiceCount
FROM Invoice
GROUP BY Supplier.Name;

-- GROUP BY with multiple columns
SELECT Document.Status, Document.Type, COUNT(*) as Count
FROM Document
GROUP BY Document.Status, Document.Type;

-- GROUP BY with HAVING
SELECT Supplier.Name, COUNT(*) as InvoiceCount, SUM(Invoice.Amount) as TotalAmount
FROM Invoice
GROUP BY Supplier.Name
HAVING COUNT(*) > 5;

-- HAVING with aggregate condition
SELECT Document.Status, AVG(Document.Amount) as AvgAmount
FROM Document
GROUP BY Document.Status
HAVING AVG(Document.Amount) > 1000;

-- ========================================================================
-- 5. ORDER BY
-- ========================================================================

-- ORDER BY single column ascending
SELECT Document.DocumentId, Document.Amount
FROM Document
ORDER BY Document.Amount ASC;

-- ORDER BY descending
SELECT Document.DocumentId, Document.Amount
FROM Document
ORDER BY Document.Amount DESC;

-- ORDER BY multiple columns
SELECT Supplier.Name, Invoice.Amount
FROM Invoice
ORDER BY Supplier.Name ASC, Invoice.Amount DESC;

-- ORDER BY with aggregate
SELECT Supplier.Name, SUM(Invoice.Amount) as TotalAmount
FROM Invoice
GROUP BY Supplier.Name
ORDER BY TotalAmount DESC;

-- ========================================================================
-- 6. DATE AND TIME FUNCTIONS
-- ========================================================================

-- FORMATDATE
SELECT Document.DocumentId, FORMATDATE(Document.CreatedDate, 'yyyy-MM-dd') as FormattedDate
FROM Document;

-- FORMATTIMESTAMP
SELECT Document.DocumentId, FORMATTIMESTAMP(Document.CreatedDate, 'yyyy-MM-dd HH:mm:ss') as FormattedTimestamp
FROM Document;

-- YEAR, MONTH, DAY
SELECT 
    Document.DocumentId,
    YEAR(Document.CreatedDate) as Year,
    MONTH(Document.CreatedDate) as Month,
    DAY(Document.CreatedDate) as Day
FROM Document;

-- ADDDAYS
SELECT Document.DocumentId, ADDDAYS(Document.CreatedDate, 30) as DueDate
FROM Document;

-- ADDMONTHS
SELECT Document.DocumentId, ADDMONTHS(Document.CreatedDate, 3) as QuarterDate
FROM Document;

-- ADDYEARS
SELECT Document.DocumentId, ADDYEARS(Document.CreatedDate, 1) as NextYear
FROM Document;

-- DATEDIFF
SELECT 
    Document.DocumentId,
    DATEDIFF('day', Document.CreatedDate, Document.CompletedDate) as DaysToComplete
FROM Document
WHERE Document.CompletedDate IS NOT NULL;

-- GETDATE (current date/time)
SELECT Document.DocumentId
FROM Document
WHERE Document.CreatedDate < GETDATE();

-- DATEPART
SELECT 
    Document.DocumentId,
    DATEPART('quarter', Document.CreatedDate) as Quarter,
    DATEPART('week', Document.CreatedDate) as Week
FROM Document;

-- DAYOFWEEK, DAYOFYEAR
SELECT 
    Document.DocumentId,
    DAYOFWEEK(Document.CreatedDate) as DayOfWeek,
    DAYOFYEAR(Document.CreatedDate) as DayOfYear
FROM Document;

-- ========================================================================
-- 7. STRING FUNCTIONS
-- ========================================================================

-- STRINGCONCAT
SELECT STRINGCONCAT(Supplier.FirstName, ' ', Supplier.LastName) as FullName
FROM Supplier;

-- SUBSTRING
SELECT Document.DocumentId, SUBSTRING(Document.Title, 1, 50) as ShortTitle
FROM Document;

-- CHARINDEX (find position of substring)
SELECT Document.DocumentId, CHARINDEX('Invoice', Document.Title) as Position
FROM Document;

-- LEN (length of string)
SELECT Document.Title, LEN(Document.Title) as TitleLength
FROM Document;

-- REPLACE
SELECT Document.DocumentId, REPLACE(Document.Title, 'Old', 'New') as UpdatedTitle
FROM Document;

-- TRIM, LTRIM, RTRIM
SELECT 
    Supplier.Name,
    TRIM(Supplier.Name) as TrimmedName,
    LTRIM(Supplier.Name) as LeftTrimmed,
    RTRIM(Supplier.Name) as RightTrimmed
FROM Supplier;

-- UPPER and LOWER
SELECT 
    Supplier.Name,
    UPPER(Supplier.Name) as UpperName,
    LOWER(Supplier.Name) as LowerName
FROM Supplier;

-- ========================================================================
-- 8. MATH FUNCTIONS
-- ========================================================================

-- ROUND
SELECT Invoice.InvoiceId, ROUND(Invoice.Amount, 2) as RoundedAmount
FROM Invoice;

-- CEILING and FLOOR
SELECT 
    Invoice.InvoiceId,
    CEILING(Invoice.Amount) as CeilingAmount,
    FLOOR(Invoice.Amount) as FloorAmount
FROM Invoice;

-- ABS (absolute value)
SELECT Document.DocumentId, ABS(Document.Amount) as AbsoluteAmount
FROM Document;

-- POWER
SELECT Document.DocumentId, POWER(Document.Amount, 2) as AmountSquared
FROM Document;

-- SQRT
SELECT Document.DocumentId, SQRT(Document.Amount) as AmountSqrt
FROM Document
WHERE Document.Amount >= 0;

-- ========================================================================
-- 9. CONDITIONAL EXPRESSIONS
-- ========================================================================

-- CASE statement
SELECT 
    Document.DocumentId,
    Document.Amount,
    CASE 
        WHEN Document.Amount > 10000 THEN 'High'
        WHEN Document.Amount > 5000 THEN 'Medium'
        ELSE 'Low'
    END as AmountCategory
FROM Document;

-- CASE with multiple conditions
SELECT 
    Document.DocumentId,
    CASE 
        WHEN Document.Status = 'Active' AND Document.Amount > 1000 THEN 'Active-High'
        WHEN Document.Status = 'Active' THEN 'Active-Low'
        WHEN Document.Status = 'Pending' THEN 'Pending'
        ELSE 'Other'
    END as StatusCategory
FROM Document;

-- IIF function
SELECT Document.DocumentId, IIF(Document.Amount > 1000, 'High', 'Low') as Category
FROM Document;

-- ISNULL (coalesce)
SELECT Document.DocumentId, ISNULL(Document.Description, 'No Description') as Description
FROM Document;

-- NULLIF
SELECT Document.DocumentId, NULLIF(Document.Amount, 0) as NonZeroAmount
FROM Document;

-- ========================================================================
-- 10. SUBQUERIES
-- ========================================================================

-- Subquery in WHERE clause
SELECT Document.DocumentId, Document.Amount
FROM Document
WHERE Document.Amount > (
    SELECT AVG(Amount) FROM Document WHERE Status = 'Active'
);

-- Subquery with IN
SELECT Supplier.Name
FROM Supplier
WHERE Supplier.SupplierId IN (
    SELECT DISTINCT SupplierId FROM Invoice WHERE Amount > 1000
);

-- Subquery in SELECT
SELECT 
    Document.DocumentId,
    Document.Amount,
    (SELECT AVG(Amount) FROM Document) as OverallAverage
FROM Document;

-- Correlated subquery
SELECT d1.DocumentId, d1.Amount
FROM Document d1
WHERE d1.Amount > (
    SELECT AVG(d2.Amount)
    FROM Document d2
    WHERE d2.Type = d1.Type
);

-- ========================================================================
-- 11. COMPLEX QUERIES
-- ========================================================================

-- Nested subqueries
SELECT Supplier.Name, Supplier.TotalAmount
FROM (
    SELECT 
        s.SupplierId,
        s.Name,
        SUM(i.Amount) as TotalAmount
    FROM Supplier s
    INNER JOIN Invoice i ON s.SupplierId = i.SupplierId
    GROUP BY s.SupplierId, s.Name
) Supplier
WHERE Supplier.TotalAmount > 10000;

-- Multiple JOINs with aggregates
SELECT 
    p.ProjectName,
    COUNT(DISTINCT d.DocumentId) as DocumentCount,
    COUNT(DISTINCT s.SupplierId) as SupplierCount,
    SUM(d.Amount) as TotalAmount,
    AVG(d.Amount) as AverageAmount
FROM Project p
LEFT JOIN Document d ON p.ProjectId = d.ProjectId
LEFT JOIN Supplier s ON d.SupplierId = s.SupplierId
WHERE p.Status = 'Active'
GROUP BY p.ProjectName
HAVING SUM(d.Amount) > 50000
ORDER BY TotalAmount DESC;

-- Complex CASE with aggregates
SELECT 
    Supplier.Region,
    SUM(CASE WHEN Invoice.Status = 'Paid' THEN Invoice.Amount ELSE 0 END) as PaidAmount,
    SUM(CASE WHEN Invoice.Status = 'Pending' THEN Invoice.Amount ELSE 0 END) as PendingAmount,
    SUM(CASE WHEN Invoice.Status = 'Overdue' THEN Invoice.Amount ELSE 0 END) as OverdueAmount
FROM Invoice
GROUP BY Supplier.Region;

-- Window functions (if supported)
SELECT 
    Document.DocumentId,
    Document.Amount,
    ROW_NUMBER() OVER (ORDER BY Document.Amount DESC) as RowNum,
    RANK() OVER (ORDER BY Document.Amount DESC) as Rank
FROM Document;

-- ========================================================================
-- 12. UNION
-- ========================================================================

-- UNION of two queries
SELECT DocumentId as Id, 'Document' as Type, Amount
FROM Document
WHERE Status = 'Active'
UNION
SELECT InvoiceId as Id, 'Invoice' as Type, Amount
FROM Invoice
WHERE Status = 'Active';

-- UNION ALL (includes duplicates)
SELECT SupplierId, Name FROM Supplier WHERE Status = 'Active'
UNION ALL
SELECT SupplierId, Name FROM Supplier WHERE Status = 'Pending';

-- ========================================================================
-- 13. DISTINCT
-- ========================================================================

-- SELECT DISTINCT
SELECT DISTINCT Supplier.Region
FROM Supplier;

-- DISTINCT with multiple columns
SELECT DISTINCT Document.Status, Document.Type
FROM Document;

-- ========================================================================
-- 14. NULL HANDLING
-- ========================================================================

-- IS NULL
SELECT Document.DocumentId, Document.Description
FROM Document
WHERE Document.Description IS NULL;

-- IS NOT NULL
SELECT Document.DocumentId, Document.CompletedDate
FROM Document
WHERE Document.CompletedDate IS NOT NULL;

-- COALESCE (first non-null value)
SELECT 
    Document.DocumentId,
    COALESCE(Document.Description, Document.Title, 'No Info') as Info
FROM Document;

-- ========================================================================
-- 15. TOP/LIMIT
-- ========================================================================

-- TOP N records
SELECT TOP 10 Document.DocumentId, Document.Amount
FROM Document
ORDER BY Document.Amount DESC;

-- LIMIT (alternative syntax)
SELECT Document.DocumentId, Document.Amount
FROM Document
ORDER BY Document.Amount DESC
LIMIT 10;

-- TOP with PERCENT
SELECT TOP 5 PERCENT Document.DocumentId, Document.Amount
FROM Document
ORDER BY Document.Amount DESC;

-- ========================================================================
-- 16. EXISTS
-- ========================================================================

-- EXISTS subquery
SELECT Supplier.Name
FROM Supplier
WHERE EXISTS (
    SELECT 1 FROM Invoice
    WHERE Invoice.SupplierId = Supplier.SupplierId
    AND Invoice.Status = 'Overdue'
);

-- NOT EXISTS
SELECT Project.ProjectName
FROM Project
WHERE NOT EXISTS (
    SELECT 1 FROM Document
    WHERE Document.ProjectId = Project.ProjectId
    AND Document.Status = 'Completed'
);

-- ========================================================================
-- 17. ARIBA-SPECIFIC PATTERNS
-- ========================================================================

-- Document fields with dot notation
SELECT 
    Document.DocumentId,
    Document.Title,
    Document.Status,
    Document.CreatedDate,
    Document.Amount,
    Document.Description
FROM Document
WHERE Document.Status = 'Active';

-- Project object references
SELECT 
    Project.ProjectId,
    Project.ProjectName,
    Project.ProjectOwner,
    Project.StartDate,
    Project.EndDate,
    Project.Status
FROM Project
WHERE Project.Status IN ('Active', 'Planning');

-- Supplier object references
SELECT 
    Supplier.SupplierId,
    Supplier.Name,
    Supplier.Region,
    Supplier.Status,
    Supplier.RegistrationDate
FROM Supplier
WHERE Supplier.Status = 'Active';

-- Invoice object references
SELECT 
    Invoice.InvoiceId,
    Invoice.InvoiceNumber,
    Invoice.Amount,
    Invoice.InvoiceDate,
    Invoice.DueDate,
    Invoice.Status
FROM Invoice
WHERE Invoice.Status = 'Pending';

-- Contract object references
SELECT 
    Contract.ContractId,
    Contract.ContractNumber,
    Contract.ContractAmount,
    Contract.StartDate,
    Contract.EndDate,
    Contract.Status
FROM Contract
WHERE Contract.Status = 'Active' AND Contract.ContractAmount > 10000;

-- Requisition object references
SELECT 
    Requisition.RequisitionId,
    Requisition.RequisitionNumber,
    Requisition.TotalAmount,
    Requisition.CreatedDate,
    Requisition.Status
FROM Requisition
WHERE Requisition.Status = 'Approved';

-- Order object references
SELECT 
    Order.OrderId,
    Order.OrderNumber,
    Order.OrderAmount,
    Order.OrderDate,
    Order.DeliveryDate,
    Order.Status
FROM Order
WHERE Order.Status = 'Fulfilled';

-- ========================================================================
-- End of AQL Example Queries
-- ========================================================================

