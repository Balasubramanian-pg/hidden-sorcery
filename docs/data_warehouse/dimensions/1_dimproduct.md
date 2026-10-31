<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## 1. `Dim_Product`

### Design Intent

This dimension quietly controls:

- Revenue skew
    
- Basket size
    
- Metro vs rural economics
    
- Product-led seasonality
    

### Hidden Mechanics Embedded

- **Metro Affinity Flag**  
    Used later to bias attachments and high-value sales
    
- **Rural Affinity Flag**  
    Drives volume-heavy, low-ticket behavior
    
- **Base Price Band**  
    Enables realistic invoice values without hardcoding prices
    

---

### Snowflake SQL

```sql
CREATE OR REPLACE TABLE Dim_Product AS
SELECT
    ROW_NUMBER() OVER (ORDER BY product_line, sub_category, model_name) AS product_key,
    product_line,
    sub_category,
    model_name,
    hp_category,
    CASE 
        WHEN product_line = 'Tractors' THEN 'HIGH'
        WHEN product_line IN ('Harvest Equipment') THEN 'VERY HIGH'
        WHEN product_line IN ('Tillers','Reapers') THEN 'MEDIUM'
        ELSE 'LOW'
    END AS base_price_band,
    CASE 
        WHEN product_line IN ('Attachments','Implements') THEN 'Y'
        ELSE 'N'
    END AS is_addon_product,
    CASE 
        WHEN product_line IN ('Tractors','Harvest Equipment') THEN 'Y'
        ELSE 'N'
    END AS is_primary_product,
    CASE 
        WHEN sub_category IN ('Compact Tractors','Tillers','Mini Tillers') THEN 'Y'
        ELSE 'N'
    END AS rural_affinity_flag,
    CASE 
        WHEN sub_category IN ('Utility Tractors','Row Crop Tractors','Attachments') THEN 'Y'
        ELSE 'N'
    END AS metro_affinity_flag
FROM (
    SELECT * FROM VALUES
    -- Tractors
    ('Tractors','Compact Tractors','CT-22','22 HP'),
    ('Tractors','Compact Tractors','CT-28','28 HP'),
    ('Tractors','Utility Tractors','UT-45','45 HP'),
    ('Tractors','Utility Tractors','UT-55','55 HP'),
    ('Tractors','Row Crop Tractors','RC-65','65 HP'),
    ('Tractors','Orchard Tractors','OT-40','40 HP'),

    -- Tillers
    ('Tillers','Mini Tillers','MT-7','7 HP'),
    ('Tillers','Power Tillers','PT-12','12 HP'),
    ('Tillers','Rotary Tillers','RT-15','15 HP'),

    -- Reapers
    ('Reapers','Self-Propelled Reapers','SPR-1','N/A'),
    ('Reapers','Tractor Mounted Reapers','TMR-2','N/A'),

    -- Harvest Equipment
    ('Harvest Equipment','Mini Harvesters','MH-90','90 HP'),
    ('Harvest Equipment','Combine Harvesters','CH-120','120 HP'),

    -- Attachments
    ('Attachments','Loaders','LD-1','N/A'),
    ('Attachments','Backhoes','BH-1','N/A'),
    ('Attachments','Dozer Blades','DB-1','N/A'),

    -- Implements
    ('Implements','Ploughs','PL-1','N/A'),
    ('Implements','Seeders','SD-1','N/A'),
    ('Implements','Sprayers','SP-1','N/A'),
    ('Implements','Cultivators','CV-1','N/A')
) AS t(product_line, sub_category, model_name, hp_category);
```

### Why This Matters Later

Without touching facts, this enables:

- Revenue vs unit divergence
    
- Add-on attach rate analysis
    
- Metro upsell detection
    
- Product mix drift by geography
    

---
