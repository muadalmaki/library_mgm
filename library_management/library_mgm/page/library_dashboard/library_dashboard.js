frappe.pages['library-dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Library Dashboard',
        single_column: true
    });

    page.add_inner_button(__('Refresh'), function() {
        // Refresh dashboard data
    });

    // Add your dashboard content here
    let $container = $('<div>').appendTo(page.body);
    
    frappe.call({
        method: 'library_management.library_management.library_mgm.library_mgm_dashboard. library_dashboard.library_dashboard.get_dashboard_data',
        callback: function(r) {
            if (r.message) {
                let data = r.message;
                $container.append(`
                    <div class="row">
                        <div class="col-sm-4">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Total Books</h5>
                                    <p class="card-text">${data.total_books}</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-4">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Books Issued</h5>
                                    <p class="card-text">${data.books_issued}</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-4">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Total Members</h5>
                                    <p class="card-text">${data.total_members}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                `);
            }
        }
    });
}
