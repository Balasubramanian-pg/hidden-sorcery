<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## 2. `Dim_Location` (Australia Only)

### Design Notes

- Australia-specific geography
    
- Normalized for BI slicing
    
- Dealer, customer, enquiry reuse
    
- No Indian fields or values
    

### States Covered

- New South Wales
    
- Victoria
    
- Queensland
    
- Western Australia
    
- South Australia
    
- Tasmania
    
- Australian Capital Territory
    
- Northern Territory
    

### Snowflake SQL

```sql
CREATE OR REPLACE TABLE Dim_Location AS
SELECT
    ROW_NUMBER() OVER (ORDER BY state, city)        AS location_key,
    'Australia'                                     AS country,
    state,
    city,
    region,
    postcode
FROM (
    SELECT * FROM VALUES
    ('New South Wales','Sydney','Greater Sydney','2000'),
    ('New South Wales','Newcastle','Hunter Region','2300'),
    ('New South Wales','Wagga Wagga','Riverina','2650'),

    ('Victoria','Melbourne','Greater Melbourne','3000'),
    ('Victoria','Geelong','Barwon','3220'),
    ('Victoria','Shepparton','Goulburn Valley','3630'),

    ('Queensland','Brisbane','South East Queensland','4000'),
    ('Queensland','Toowoomba','Darling Downs','4350'),
    ('Queensland','Rockhampton','Central Queensland','4700'),

    ('Western Australia','Perth','Greater Perth','6000'),
    ('Western Australia','Bunbury','South West','6230'),
    ('Western Australia','Kalgoorlie','Goldfields','6430'),

    ('South Australia','Adelaide','Greater Adelaide','5000'),
    ('South Australia','Mount Gambier','Limestone Coast','5290'),

    ('Tasmania','Hobart','Southern Tasmania','7000'),
    ('Tasmania','Launceston','Northern Tasmania','7250'),

    ('Australian Capital Territory','Canberra','ACT','2600'),

    ('Northern Territory','Darwin','Top End','0800'),
    ('Northern Territory','Alice Springs','Central Australia','0870')
) AS t(state, city, region, postcode);
```

### Validation Check

- Clean surrogate key
    
- No duplicates
    
- BI-friendly grain
    
- Reusable across all facts
    

---
