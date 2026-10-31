<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## 4. `Fact_Enquiries`

### Grain

**One row per enquiry**

### Measures

- Enquiry count
    
- Conversion flag
    
- Lag to conversion (derived later)
    

---

### Snowflake SQL

```sql
CREATE OR REPLACE TABLE Fact_Enquiries AS
SELECT
    enquiry_key,
    enquiry_number,
    enquiry_date_key,
    customer_key,
    dealer_key,
    product_key,
    enquiry_stage,
    is_converted,
    next_followup_date_key
FROM (
    SELECT
        ROW_NUMBER() OVER (ORDER BY enquiry_number)          AS enquiry_key,
        'ENQ-' || LPAD(SEQ4()+1000000, 8, '0')               AS enquiry_number,
        dd.date_key                                         AS enquiry_date_key,
        dc.customer_key,
        dlr.dealer_key,
        dp.product_key,
        enquiry_stage,
        CASE 
            WHEN enquiry_stage = 'CONVERTED' THEN 'Y'
            ELSE 'N'
        END                                                  AS is_converted,
        CASE 
            WHEN enquiry_stage IN ('FOLLOW_UP','CONTACTED')
            THEN dd.date_key + UNIFORM(7,45,RANDOM())
            ELSE NULL
        END                                                  AS next_followup_date_key
    FROM (
        SELECT
            dd.date_key,
            dc.customer_key,
            dlr.dealer_key,
            dp.product_key,
            CASE
                WHEN r <= 14 THEN 'CONVERTED'
                WHEN r <= 32 THEN 'FOLLOW_UP'
                WHEN r <= 55 THEN 'CONTACTED'
                WHEN r <= 72 THEN 'QUALIFIED'
                ELSE 'DROPPED'
            END AS enquiry_stage
        FROM Dim_Date dd
        JOIN TABLE(GENERATOR(ROWCOUNT => 1800000))
        JOIN Dim_Customer dc
            ON UNIFORM(1,100,RANDOM()) <= 85
        JOIN Dim_Dealer dlr
            ON UNIFORM(1,100,RANDOM()) <= 
               CASE WHEN dlr.location_type = 'RURAL' THEN 78 ELSE 42 END
        JOIN Dim_Product dp
            ON UNIFORM(1,100,RANDOM()) <= 
               CASE 
                   WHEN dlr.location_type = 'RURAL' AND dp.rural_affinity_flag = 'Y' THEN 75
                   WHEN dlr.location_type = 'METRO' AND dp.metro_affinity_flag = 'Y' THEN 70
                   ELSE 30
               END
        CROSS JOIN (
            SELECT UNIFORM(1,100,RANDOM()) AS r
        )
        WHERE dd.full_date BETWEEN '2021-01-23' AND '2026-01-23'
    )
);
```

---
