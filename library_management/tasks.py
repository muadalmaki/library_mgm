import frappe
from frappe.utils import today

def check_membership_validity():
    memberships = frappe.get_all("Library Membership", filters={"to_date": ["<", today()]}, fields=["library_member"])
    for membership in memberships:
        customer = frappe.get_doc("Customer", membership.library_member)
        customer.is_membership_valid = 0
        customer.save()
