<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## 1. Funnel Design (Explicit and Intentional)

### Customer Mix

- **B2C: 82%**
    
- **B2B: 18%**
    

This is enforced at customer creation time, not enquiry time.  
This matters because repeat behaviour attaches to the customer, not the lead.

### Repeat Enquiry Behaviour

- Customers may generate **multiple enquiries**
    
- Repeat probability is:
    
    - Higher for B2C rural customers
        
    - Lower but higher-value for B2B metro customers
        
- This is **probabilistic**, not deterministic
    
- No fixed “repeat customer flag”
    

This ensures:

- No obvious pattern
    
- Requires SQL to discover
    

### Sales Funnel Stages (Standardized)

Each enquiry will land in **one and only one terminal stage**.

Stages:

- `NEW`
    
- `CONTACTED`
    
- `FOLLOW_UP`
    
- `QUALIFIED`
    
- `DROPPED`
    
- `CONVERTED`
    

Rules:

- `CONVERTED` enquiries will later appear in `Fact_Billing`
    
- `DROPPED` are dead leads
    
- `FOLLOW_UP` creates pipeline carryover
    
- Stage progression is **not linear for all records**
    

---
