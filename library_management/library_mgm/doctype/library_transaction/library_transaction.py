from frappe.model.document import Document
import frappe
from frappe import _

class LibraryTransaction(Document):
    def validate(self):
        self.validate_membership()
        self.validate_maximum_limit()

    def validate_membership(self):
        customer = frappe.get_doc("Customer", self.library_member)
        if not customer.is_library_member:
            frappe.throw(_("The member is not registered as a library member"))
        if not customer.is_membership_valid:
            frappe.throw(_("The member does not have a valid membership"))

    def validate_maximum_limit(self):
        settings = frappe.get_last_doc("Library Management Settings")
        if self.transaction_type == "Issue":
            count = frappe.db.count(
                "Library Transaction",
                {"library_member": self.library_member, "transaction_type": "Issue", "docstatus": 1},
            )
            if count >= settings.loan_period:
                frappe.throw(_("Maximum limit reached for issuing articles"))

    def on_submit(self):
        if self.transaction_type == "Issue":
            article = frappe.get_doc("Article", self.article)
            article.status = "Issued"
            article.save()

    def on_cancel(self):
        if self.transaction_type == "Issue":
            article = frappe.get_doc("Article", self.article)
            article.status = "Available"
            article.save()
