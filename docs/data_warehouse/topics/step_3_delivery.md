<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## Step 3 Delivery

### Snowflake SQL for `Dim_Customer` and `Fact_Enquiries`

You were very explicit here, so I will be equally precise.  
This step **locks the sales funnel semantics** into the data model so that downstream analysis feels real, not manufactured.

I will structure this in four parts:

1. Funnel design decisions (so you know exactly what is encoded)
    
2. `Dim_Customer`
    
3. Enquiry stage model (important)
    
4. `Fact_Enquiries` SQL
    

No assumptions will be hidden.

---
