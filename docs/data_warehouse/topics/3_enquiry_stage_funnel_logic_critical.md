<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## 3. Enquiry Stage & Funnel Logic (Critical)

### Monthly Conversion Distortion

Each enquiry month is tagged internally with a **conversion pressure band**:

- High months → ≥60% eventual conversion
    
- Medium months → 30–45%
    
- Weak months → 13–20%
    

This will **not be stored explicitly**.  
It will emerge only through aggregation.

### Rural vs Metro Impact

- Rural:
    
    - More enquiries
        
    - More `FOLLOW_UP`
        
    - Longer stage duration
        
- Metro:
    
    - Fewer enquiries
        
    - Faster `CONVERTED` or `DROPPED`
        

---
