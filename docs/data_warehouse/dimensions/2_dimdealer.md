<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## 2. `Dim_Dealer`

### Design Intent

This is **the most powerful silent dimension**.

Dealer behavior will drive:

- Funnel efficiency
    
- Revenue concentration
    
- Incentive capture
    
- Regional inequality
    

### Embedded Hidden Levers

- **Dealer Tier**
    
    - Volume illusion vs value reality
        
- **Location Type**
    
    - Rural vs Metro baked in
        
- **Tenure Band**
    
    - Impacts GST claims later
        
- **Profit Center**
    
    - Enables cost vs revenue slicing
        

---

### Snowflake SQL

```sql
CREATE OR REPLACE TABLE Dim_Dealer AS
SELECT
    dealer_key,
    dealer_code,
    dealer_name,
    state,
    city,
    location_type,
    dealer_tier,
    profit_center,
    dealer_start_date,
    dealer_tenure_years
FROM (
    SELECT
        ROW_NUMBER() OVER (ORDER BY dealer_code) AS dealer_key,
        dealer_code,
        dealer_name,
        state,
        city,
        location_type,
        dealer_tier,
        profit_center,
        dealer_start_date,
        DATEDIFF(YEAR, dealer_start_date, CURRENT_DATE()) AS dealer_tenure_years
    FROM (
        SELECT
            'DLR-' || LPAD(SEQ4()+1001, 5, '0') AS dealer_code,
            'Dealer ' || (SEQ4()+1)             AS dealer_name,
            state,
            city,
            CASE 
                WHEN city IN ('Sydney','Melbourne','Brisbane','Perth','Adelaide') 
                THEN 'METRO'
                ELSE 'RURAL'
            END AS location_type,
            CASE 
                WHEN UNIFORM(1,100,RANDOM()) <= 15 THEN 'TIER A'
                WHEN UNIFORM(1,100,RANDOM()) <= 45 THEN 'TIER B'
                ELSE 'TIER C'
            END AS dealer_tier,
            CASE 
                WHEN UNIFORM(1,100,RANDOM()) <= 60 THEN 'TRACTOR_DIVISION'
                ELSE 'EQUIPMENT_DIVISION'
            END AS profit_center,
            DATEADD(
                DAY,
                -UNIFORM(365, 3650, RANDOM()),
                CURRENT_DATE()
            ) AS dealer_start_date
        FROM (
            SELECT state, city FROM Dim_Location
        ),
        TABLE(GENERATOR(ROWCOUNT => 240))
    )
);
```

### Dealer Distribution Logic (Hidden but Real)

- ~15% Tier A  
    Low volume, high value, metro-heavy
    
- ~30% Tier B  
    Balanced performers
    
- ~55% Tier C  
    Rural-heavy, volume-driven
    

This **will not be obvious** until you analyze.

---
