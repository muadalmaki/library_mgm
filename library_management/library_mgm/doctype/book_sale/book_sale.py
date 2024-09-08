from frappe.model.document import Document
import frappe

class BookSale(Document):
    def validate(self):
        self.calculate_total()
        self.check_inventory()

    def on_submit(self):
        self.update_inventory()

    def calculate_total(self):
        self.total_amount = sum(item.amount or 0 for item in self.items)

    def check_inventory(self):
        for item in self.items:
            inventory = frappe.get_all(
                "Book Inventory",
                filters={"article": item.article},
                fields=["quantity"]
            )
            if not inventory or inventory[0].quantity < item.quantity:
                frappe.throw(f"Insufficient inventory for article {item.article}")

    def update_inventory(self):
        for item in self.items:
            inventory_list = frappe.get_all(
                "Book Inventory",
                filters={"article": item.article},
                fields=["name", "quantity"]
            )
            if inventory_list:
                inventory = frappe.get_doc("Book Inventory", inventory_list[0].name)
                inventory.quantity -= item.quantity
                inventory.save()
            else:
                frappe.throw(f"No inventory record found for article {item.article}")
