import frappe
from frappe.utils import get_url_to_form

def send_membership_expiry_notification():
    today = frappe.utils.today()
    members = frappe.get_all(
        "Library Membership",
        filters={"to_date": ("<=", frappe.utils.add_days(today, 7))},
        fields=["name", "library_member", "to_date"]
    )

    for member in members:
        member_name = frappe.get_value("Customer", member.library_member, "customer_name")
        expiry_date = member.to_date
        notification_message = f"Dear {member_name}, your library membership is expiring on {expiry_date}. Please renew it soon!"

        doc_url = get_url_to_form("Library Membership", member.name)
        notification_message += f"\n\nYou can renew your membership here: {doc_url}"


        frappe.sendmail(
            recipients=[frappe.get_value("Customer", member.library_member, "email_id")],
            subject="Library Membership Expiry Notification",
            message=notification_message
        )

