from frappe.model.document import Document
import frappe
from frappe import _

class LibraryMembership(Document):
    def validate(self):
        self.validate_dates()
        self.validate_membership()

    def validate_dates(self):
        if self.from_date > self.to_date:
            frappe.throw(_("To Date cannot be before From Date"))

    def validate_membership(self):
        existing = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "to_date": (">", self.from_date),
            },
        )
        if existing:
            frappe.throw(_("There is an active membership for this member"))

    def on_submit(self):
        if self.paid:
            customer = frappe.get_doc("Customer", self.library_member)
            customer.is_membership_valid = 1
            customer.save()

    def on_cancel(self):
        customer = frappe.get_doc("Customer", self.library_member)
        customer.is_membership_valid = 0
        customer.save()
