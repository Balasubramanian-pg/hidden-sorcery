<!-- markdown-splitter:generated -->
[← Back to source index](../../../data_warehouse.md)

## Target Warehouse Structure (Confirmed)

### Dimension Tables

#### 1. Dim_Dealer

Purpose: Dealer master data

Typical attributes:

- Dealer Code
    
- Dealer Name
    
- Dealership Name
    
- Profit Center
    
- Dealer Status
    
- Dealer Start Date
    
- Dealer Location Key
    
- Active Flag
    

#### 2. Dim_Customer

Purpose: End-customer master

Typical attributes:

- Customer Code
    
- Customer Name
    
- Mobile Number
    
- Customer Type (Individual, Farm, Business)
    
- Location Key
    
- Created Date
    

#### 3. Dim_Product

Purpose: Product catalog

Typical attributes:

- Product Code
    
- Model Name
    
- HP Category
    
- Product Line (Tractor, Tiller, Reaper)
    
- Material Group
    
- Launch Date
    
- Discontinued Flag
    

#### 4. Dim_Date

Purpose: Time intelligence

Attributes:

- Date Key
    
- Date
    
- Day
    
- Month
    
- Month Name
    
- Quarter
    
- Financial Year
    
- Calendar Year
    
- Is Weekend
    

#### 5. Dim_Location

Purpose: Geography normalization

Attributes:

- Location Key
    
- State
    
- District / Region
    
- City / Town
    
- Postcode
    
- Country (Australia fixed)
    

### Fact Tables

#### 1. Fact_Billing

Grain: **One row per billing document per product**

Derived from:

- Billing documents
    
- Sold-to / ship-to
    
- Quantity, amount
    

Measures:

- Quantity
    
- Invoice Amount
    
- Billing Count
    

#### 2. Fact_Production

Grain: **One row per produced unit**

Derived from:

- Plant records
    
- Serial numbers
    
- Engine / chassis
    

Measures:

- Units Produced
    

#### 3. Fact_GST_Invoices

Grain: **One row per activity claim invoice**

Derived from:

- Activity Claim GST Invoice Report
    

Measures:

- Approved Claim Amount
    
- Invoice Amount
    
- Credit Note Amount
    

#### 4. Fact_Enquiries

Grain: **One row per enquiry**

Derived from:

- CRM / Digital / Field enquiries
    

Measures:

- Enquiry Count
    
- Converted Flag (derived later)
    

#### 5. Fact_DeliveryChallans

Grain: **One row per delivery**

Derived from:

- DC numbers
    
- VIN / Chassis
    

Measures:

- Delivered Units
    

This is a **textbook but realistic enterprise warehouse**.

You are doing the right thing.
