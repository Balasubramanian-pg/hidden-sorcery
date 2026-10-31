<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## Conversion & Funnel Logic (This Is the Core)

You want a **non-flat, realistic monthly funnel**, not a fake constant rate.

I will encode the following **explicit logic**.

### Monthly Behaviour Pattern

Each calendar year will have:

- **3 high-conversion months**
    
    - Conversion ≥ **60%**
        
- **5 medium months**
    
    - Conversion between **30%–45%**
        
- **4 weak months**
    
    - Conversion between **13%–20%**
        

This pattern will **shift year to year**, not repeat mechanically.

### Lead-Level Logic (Your Rule Implemented Exactly)

For every **7 enquiries**:

- **1 converts in the same month**
    
- **4 are followed up into next months**
    
- **2 never convert**
    

Of the 4 followed-up:

- Some convert next month
    
- Some convert after 2–4 months
    
- Some eventually die
    

This creates:

- Backlog
    
- Pipeline carryover
    
- Lagged revenue
    
- Realistic month-to-month variance
    

This logic will drive:

- `Fact_Enquiries`
    
- `Fact_Billing`
    
- `Fact_DeliveryChallans`
    

---
