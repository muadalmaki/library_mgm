frappe.ui.form.on('Library Membership', {
    refresh: function(frm) {
        frm.set_query('library_member', function() {
            return {
                filters: {
                    is_membership_valid: 0
                }
            };
        });
    }
});

