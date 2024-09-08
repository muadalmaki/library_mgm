import frappe

@frappe.whitelist()
def get_dashboard_data():
    total_books = frappe.db.count('Article')
    books_issued = frappe.db.count('Library Transaction', {'transaction_type': 'Issue', 'docstatus': 1})
    total_members = frappe.db.count('Customer', {'is_library_member': 1})

    return {
        'total_books': total_books,
        'books_issued': books_issued,
        'total_members': total_members
    }
