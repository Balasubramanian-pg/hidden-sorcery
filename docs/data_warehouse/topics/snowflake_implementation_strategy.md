<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## Snowflake Implementation Strategy

Everything will be delivered as **Snowflake-native SQL** using:

- `TABLE(GENERATOR())`
    
- `SEQ4()`
    
- `DATEADD`
    
- `UNIFORM`, `RANDOM`
    
- Deterministic keys
    
- Repeatable logic
    

### Dimension Tables (First)

1. `Dim_Date`
    
2. `Dim_Location`
    
3. `Dim_Product`
    
4. `Dim_Dealer`
    
5. `Dim_Customer`
    

Each built using `CREATE TABLE AS SELECT`.

### Fact Tables (Second)

1. `Fact_Enquiries`
    
2. `Fact_Billing`
    
3. `Fact_DeliveryChallans`
    
4. `Fact_GST_Invoices`
    
5. `Fact_Production`
    

Facts will:

- Reference dimension surrogate keys
    
- Respect grain definitions
    
- Maintain temporal integrity
    

---
