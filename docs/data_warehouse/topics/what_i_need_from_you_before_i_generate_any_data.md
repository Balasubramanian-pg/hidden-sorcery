<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## What I Need From You Before I Generate Any Data

I will **not guess** these. Answering these once saves multiple rewrites.

### 1. Financial Year Definition (Critical)

Choose one:

- Australian FY: **1 July – 30 June**
    
- Calendar Year: **1 Jan – 31 Dec**
    

State explicitly.

### 2. Exact 5-Year Window

Pick one:

- Example: FY2020–FY2024
    
- Example: FY2021–FY2025
    
- Example: FY2022–FY2026
    

### 3. Approximate Scale (Very Important)

Give ranges, not exact numbers.

Per year:

- Number of dealers
    
- Number of enquiries
    
- Number of invoices
    
- Number of delivered units
    

Example answer:

- Dealers: 60–80
    
- Enquiries: 12,000–18,000 per year
    
- Sales invoices: 3,000–4,000 per year
    

### 4. Conversion Logic

Confirm yes or no:

- Enquiry → Billing is **not 1:1**
    
- Some enquiries never convert
    
- Some convert after weeks or months
    

If yes, I will model funnel drop-offs realistically.

### 5. Product Mix (Simple % Is Enough)

Approximate split:

- Tractors %
    
- Tillers %
    
- Reapers %
    

Example:

- Tractors 65%
    
- Tillers 25%
    
- Reapers 10%
    

### 6. Output Format (Choose One or More)

- Snowflake SQL (`CREATE TABLE AS SELECT`)
    
- CSV-style tables
    
- Separate SQL per dimension and fact
    
- Single master script
