<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## 1. `Dim_Date`

### Design Notes

- Calendar year model
    
- Date range: **23-Jan-2021 → 23-Jan-2026**
    
- Surrogate `date_key` in `YYYYMMDD` format
    
- Analytics-ready attributes
    
- No assumptions hidden
    

### Snowflake SQL

```sql
CREATE OR REPLACE TABLE Dim_Date AS
SELECT
    TO_NUMBER(TO_CHAR(d, 'YYYYMMDD'))              AS date_key,
    d                                              AS full_date,
    EXTRACT(YEAR FROM d)                            AS calendar_year,
    EXTRACT(MONTH FROM d)                           AS month_number,
    TO_CHAR(d, 'Month')                             AS month_name,
    EXTRACT(DAY FROM d)                             AS day_of_month,
    EXTRACT(QUARTER FROM d)                         AS quarter,
    CASE 
        WHEN EXTRACT(MONTH FROM d) BETWEEN 1 AND 3  THEN 'Q1'
        WHEN EXTRACT(MONTH FROM d) BETWEEN 4 AND 6  THEN 'Q2'
        WHEN EXTRACT(MONTH FROM d) BETWEEN 7 AND 9  THEN 'Q3'
        ELSE 'Q4'
    END                                             AS quarter_name,
    DAYOFWEEK(d)                                    AS day_of_week_number,
    TO_CHAR(d, 'DY')                                AS day_of_week_name,
    CASE 
        WHEN DAYOFWEEK(d) IN (6,7) THEN 'Y'
        ELSE 'N'
    END                                             AS is_weekend,
    CASE 
        WHEN EXTRACT(MONTH FROM d) IN (3,6,9,12) THEN 'Y'
        ELSE 'N'
    END                                             AS is_quarter_end,
    CASE 
        WHEN d = LAST_DAY(d) THEN 'Y'
        ELSE 'N'
    END                                             AS is_month_end
FROM (
    SELECT DATEADD(
        DAY,
        SEQ4(),
        DATE '2021-01-23'
    ) AS d
    FROM TABLE(GENERATOR(ROWCOUNT => 1827))
);
```

### Validation Check

- 1827 rows
    
- No gaps
    
- No future spillover
    
- Fully deterministic
    

---
