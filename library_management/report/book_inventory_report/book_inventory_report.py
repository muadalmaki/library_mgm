import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "article", "label": "Article", "fieldtype": "Link", "options": "Article", "width": 200},
        {"fieldname": "quantity", "label": "Quantity", "fieldtype": "Int", "width": 100},
        {"fieldname": "cost_price", "label": "Cost Price", "fieldtype": "Currency", "width": 120},
        {"fieldname": "selling_price", "label": "Selling Price", "fieldtype": "Currency", "width": 120},
        {"fieldname": "supplier", "label": "Supplier", "fieldtype": "Link", "options": "Supplier", "width": 200}
    ]

    data = frappe.get_all(
        "Book Inventory",
        fields=["article", "quantity", "cost_price", "selling_price", "supplier"]
    )

    return columns, data
