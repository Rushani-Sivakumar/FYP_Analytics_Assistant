"""Shared vocabulary. Prices are rough LKR placeholders - adjust to real shop prices later."""
from dataclasses import dataclass

LABELS = ["product_name", "product_category", "quantity", "unit_price", "total_amount",
          "transaction_date", "stock_level", "reorder_level", "supplier_name",
          "invoice_id", "cost_price", "unit_of_measure", "other"]

TABLE_TYPES = ["sales", "inventory", "purchases"]

TABLE_SCHEMAS = {
    "sales": ["invoice_id", "transaction_date", "product_name", "product_category",
              "quantity", "unit_of_measure", "unit_price", "total_amount"],
    "inventory": ["product_name", "product_category", "stock_level", "reorder_level",
                  "unit_of_measure", "cost_price", "unit_price"],
    "purchases": ["invoice_id", "transaction_date", "supplier_name", "product_name",
                  "quantity", "unit_of_measure", "cost_price", "total_amount"],
}


@dataclass(frozen=True)
class Product:
    name: str; category: str; unit: str; price: float; local: str; pack: str


PRODUCTS = [Product(*t) for t in [
    ("Sugar", "Dry Goods", "kg", 270, "Seeni", "1kg"),
    ("Red Dhal", "Dry Goods", "kg", 310, "Parippu", "1kg"),
    ("Samba Rice", "Dry Goods", "kg", 240, "Samba", "1kg"),
    ("Nadu Rice", "Dry Goods", "kg", 220, "Nadu", "1kg"),
    ("Wheat Flour", "Dry Goods", "kg", 230, "Piti", "1kg"),
    ("Green Gram", "Dry Goods", "kg", 580, "Mung", "1kg"),
    ("Salt", "Dry Goods", "pack", 100, "Lunu", "1kg"),
    ("Dried Fish", "Dry Goods", "pack", 650, "Karawala", "250g"),
    ("Coconut Oil", "Oils", "l", 950, "Pol Tel", "1L"),
    ("Vegetable Oil", "Oils", "l", 890, "Thel", "1L"),
    ("Tea Leaves", "Beverages", "pack", 420, "Thee", "400g"),
    ("Mineral Water", "Beverages", "pcs", 100, "Watura", "500ml"),
    ("Soft Drink", "Beverages", "pcs", 220, "Soda", "1L"),
    ("Milk Powder", "Dairy", "pack", 980, "Kiri Piti", "400g"),
    ("Chilli Powder", "Spices", "pack", 350, "Miris Kudu", "250g"),
    ("Turmeric Powder", "Spices", "pack", 220, "Kaha", "100g"),
    ("Curry Powder", "Spices", "pack", 260, "Thuna Paha", "250g"),
    ("Coconut", "Fresh", "pcs", 110, "Pol", ""),
    ("Eggs", "Fresh", "pcs", 35, "Bittara", ""),
    ("Bread", "Bakery", "pcs", 160, "Paan", "450g"),
    ("Instant Noodles", "Packaged", "pcs", 140, "Noodles", ""),
    ("Biscuits", "Packaged", "pack", 120, "Biscuit", "200g"),
    ("Soap", "Household", "pcs", 130, "Sabun", "100g"),
    ("Dish Wash Liquid", "Household", "pcs", 340, "Dishwash", "500ml"),
    ("Laundry Detergent", "Household", "pack", 480, "Sabun Piti", "1kg"),
]]

SUPPLIERS = ["Ceylon Traders", "Lanka Wholesale", "Perera & Sons", "Silva Distributors",
             "Kandy Agro Supplies", "Ruwan Enterprises", "Nimal Stores", "Colombo Foods (Pvt) Ltd"]

# The LAST TWO aliases of each label are reserved for the TEST split only,
# so the test set contains header names the model never saw in training.
ALIASES = {
    "product_name":     ["Product", "Item", "Item Name", "Product Name", "Description", "Particulars", "Itm", "Goods"],
    "product_category": ["Category", "Cat", "Item Category", "Group", "Dept", "Class", "Section", "Type"],
    "quantity":         ["Qty", "Quantity", "Qty Sold", "Qnty", "No of Items", "Nos", "Count", "Pcs"],
    "unit_price":       ["Price", "Unit Price", "Rate", "Selling Price", "Price/Unit", "U.Price", "Sell Rate", "MRP"],
    "total_amount":     ["Total", "Amount", "Line Total", "Total Amount", "Value", "Total Rs", "Sub Total", "Net"],
    "transaction_date": ["Date", "Txn Date", "Sale Date", "Bill Date", "Purchase Date", "Date of Sale", "Dt", "Day"],
    "stock_level":      ["Stock", "Stock Qty", "On Hand", "Balance", "Qty in Stock", "Closing Stock", "Available", "Bal"],
    "reorder_level":    ["Reorder", "Reorder Level", "Min Stock", "Re-order Qty", "Min Qty", "Safety Stock", "ROL", "Min"],
    "supplier_name":    ["Supplier", "Vendor", "Supplier Name", "From", "Dealer", "Distributor", "Sup", "Party"],
    "invoice_id":       ["Invoice", "Bill No", "Inv No", "Receipt No", "Invoice No", "Voucher", "Bill #", "Txn ID"],
    "cost_price":       ["Cost", "Cost Price", "Buying Price", "Purchase Price", "Unit Cost", "Buy Rate", "C.Price", "Cost/Unit"],
    "unit_of_measure":  ["Unit", "UOM", "Measure", "Unit Type", "Units of Measure", "Per", "Mu", "U/M"],
    "other":            ["Notes", "Remarks", "Comment", "Ref Code", "Row", "S.No", "#", "Misc"],
}