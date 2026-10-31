<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## 2. `Dim_Customer`

### Design Intent

This dimension enables:

- B2B vs B2C analysis
    
- Repeat behaviour
    
- Revenue concentration
    
- Sales team effectiveness by customer type
    

### Snowflake SQL

```sql
CREATE OR REPLACE TABLE Dim_Customer AS
SELECT
    customer_key,
    customer_code,
    customer_name,
    customer_type,
    primary_location_key,
    customer_created_date
FROM (
    SELECT
        ROW_NUMBER() OVER (ORDER BY customer_code) AS customer_key,
        customer_code,
        customer_name,
        customer_type,
        location_key AS primary_location_key,
        customer_created_date
    FROM (
        SELECT
            'CUST-' || LPAD(SEQ4()+100000, 7, '0')      AS customer_code,
            CASE 
                WHEN customer_type = 'B2B' 
                THEN 'Business ' || (SEQ4()+1)
                ELSE 'Customer ' || (SEQ4()+1)
            END                                        AS customer_name,
            customer_type,
            location_key,
            DATEADD(
                DAY,
                -UNIFORM(30, 1500, RANDOM()),
                CURRENT_DATE()
            )                                          AS customer_created_date
        FROM (
            SELECT
                location_key,
                CASE 
                    WHEN UNIFORM(1,100,RANDOM()) <= 82 THEN 'B2C'
                    ELSE 'B2B'
                END AS customer_type
            FROM Dim_Location
            JOIN TABLE(GENERATOR(ROWCOUNT => 120000))
        )
    )
);
```

### What This Quietly Enables

- Repeat enquiry analysis
    
- Customer lifetime modelling
    
- B2B revenue concentration
    
- Rural B2C volume illusion
    

---
