from frappe.model.document import Document
import frappe

class BookPurchaseOrder(Document):
    def validate(self):
        self.calculate_total()

    def on_submit(self):
        self.update_inventory()

    def calculate_total(self):
        self.total_amount = sum(item.amount or 0 for item in self.items)

    def update_inventory(self):
        for item in self.items:
            existing_inventory = frappe.get_all(
                "Book Inventory",
                filters={"article": item.article},
                fields=["name", "quantity"]
            )
            
            if existing_inventory:
                inventory = frappe.get_doc("Book Inventory", existing_inventory[0].name)
                inventory.quantity += item.quantity
                inventory.cost_price = item.rate  # Update cost price
                inventory.save()
            else:
                frappe.get_doc({
                    "doctype": "Book Inventory",
                    "article": item.article,
                    "quantity": item.quantity,
                    "cost_price": item.rate,
                    "supplier": self.supplier
                }).insert()

            # Update Article cost price
            article = frappe.get_doc("Article", item.article)
            article.cost_price = item.rate
            article.save()
