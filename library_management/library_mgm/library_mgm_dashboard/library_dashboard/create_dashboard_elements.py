import frappe

def create_total_articles_card():
    total_articles = frappe.db.count("Article")
    
    doc = frappe.get_doc({
        "doctype": "Article", 
        "article_name": "Total Articles", 
        "author": "System",  
        "publisher": "Library",  
        "isbn": "000-0000000000", 
        "cost_price": 0, 
        "selling_price": 0,  
        "description": f"Total number of articles: {total_articles}"
    })
    doc.insert(ignore_permissions=True)

def create_books_issued_card():
    books_issued = frappe.db.count("Library Transaction")  
    doc = frappe.get_doc({
        "doctype": "Article",
        "article_name": "Books Issued",
        "author": "System",
        "publisher": "Library",
        "isbn": "000-0000000001",
        "cost_price": 0,
        "selling_price": 0,
        "description": f"Number of books issued: {books_issued}"
    })
    doc.insert(ignore_permissions=True)

def create_total_members_card():
    total_members = frappe.db.count("Library Membership")
    
    doc = frappe.get_doc({
        "doctype": "Article",
        "article_name": "Total Members",
        "author": "System",
        "publisher": "Library",
        "isbn": "000-0000000002",
        "cost_price": 0,
        "selling_price": 0,
        "description": f"Total number of members: {total_members}"
    })
    doc.insert(ignore_permissions=True)

def create_charts_and_cards():
    create_total_articles_card()
    create_books_issued_card()
    create_total_members_card()
