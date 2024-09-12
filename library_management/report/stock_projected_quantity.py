import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        filters = {}
    
    if not filters.get("company"):
        frappe.throw(_("Please select a Company"))
    
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    return columns, data, None, chart

def get_columns():
    return [
        {"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 140},
        {"label": _("Item Name"), "fieldname": "item_name", "width": 140},
        {"label": _("Item Group"), "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "width": 120},
        {"label": _("UOM"), "fieldname": "stock_uom", "fieldtype": "Link", "options": "UOM", "width": 80},
        {"label": _("Brand"), "fieldname": "brand", "fieldtype": "Link", "options": "Brand", "width": 100},
        {"label": _("Warehouse"), "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse", "width": 120},
        {"label": _("Actual Qty"), "fieldname": "actual_qty", "fieldtype": "Float", "width": 100, "convertible": 1},
        {"label": _("Planned Qty"), "fieldname": "planned_qty", "fieldtype": "Float", "width": 100, "convertible": 1},
        {"label": _("Ordered Qty"), "fieldname": "ordered_qty", "fieldtype": "Float", "width": 100, "convertible": 1},
        {"label": _("Reserved Qty"), "fieldname": "reserved_qty", "fieldtype": "Float", "width": 100, "convertible": 1},
        {"label": _("Projected Qty"), "fieldname": "projected_qty", "fieldtype": "Float", "width": 100, "convertible": 1},
        {"label": _("Reorder Level"), "fieldname": "reorder_level", "fieldtype": "Float", "width": 100, "convertible": 1},
        {"label": _("Days of Stock"), "fieldname": "days_of_stock", "fieldtype": "Int", "width": 100},
        {"label": _("Stock Value"), "fieldname": "stock_value", "fieldtype": "Currency", "width": 120},
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    
    query = """
        SELECT 
            i.item_code, i.item_name, i.item_group, i.stock_uom, i.brand,
            b.warehouse, b.actual_qty, b.planned_qty, b.ordered_qty, b.reserved_qty, b.projected_qty,
            i.reorder_level, i.valuation_rate
        FROM 
            `tabItem` i
        LEFT JOIN 
            `tabBin` b ON i.item_code = b.item_code
        WHERE 
            b.actual_qty > 0
    """
    
    if conditions:
        query += " AND " + conditions

    data = frappe.db.sql(query, filters, as_dict=1)

    for item in data:
        item.days_of_stock = calculate_days_of_stock(item)
        item.stock_value = flt(item.actual_qty) * flt(item.valuation_rate)
    
    return data

def get_conditions(filters):
    conditions = []
    if filters.get("company"):
        conditions.append("i.company = %(company)s")
    if filters.get("warehouse"):
        conditions.append("b.warehouse = %(warehouse)s")
    if filters.get("item_code"):
        conditions.append("i.item_code = %(item_code)s")
    if filters.get("item_group"):
        conditions.append("i.item_group = %(item_group)s")
    if filters.get("brand"):
        conditions.append("i.brand = %(brand)s")
    if filters.get("low_stock"):
        conditions.append("b.actual_qty <= i.reorder_level")
    
    return " AND ".join(conditions)

def calculate_days_of_stock(item):
    if item.actual_qty and item.projected_qty is not None:
        consumption_rate = max((item.actual_qty - item.projected_qty) / 30, 0.01)  # Avoid division by zero
        return int(item.actual_qty / consumption_rate)
    return 0

def get_chart_data(data):
    labels = []
    actual_qty = []
    projected_qty = []

    for item in data[:20]:  # Limit to top 20 items for better visualization
        labels.append(item.item_code)
        actual_qty.append(item.actual_qty)
        projected_qty.append(item.projected_qty)

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": "Actual Quantity", "values": actual_qty},
                {"name": "Projected Quantity", "values": projected_qty}
            ]
        },
        "type": "bar",
        "colors": ["#d3f8d3", "#b7e8b7"]
    }
