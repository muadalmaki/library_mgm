from frappe import _

def get_data():
    return {
        'fieldname': 'library_dashboard',
        'transactions': [
            {
                'label': _('Transactions'),
                'items': ['Book', 'Library Member', 'Library Transaction']
            },
        ],
        'charts': [
            {
                'name': 'book_transactions',
                'chart_name': _('Book Transactions'),
                'chart_type': 'Count',
                'doctype': 'Library Transaction',
                'group_by_field': 'transaction_type',
                'time_interval': 'Monthly',
                'timespan': 'Last Year',
            },
            {
                'name': 'top_books',
                'chart_name': _('Top Books'),
                'chart_type': 'Group By',
                'doctype': 'Library Transaction',
                'group_by_field': 'book',
                'aggregate_function_field': 'COUNT(*)',
                'number_of_groups': 5,
            }
        ]
    }