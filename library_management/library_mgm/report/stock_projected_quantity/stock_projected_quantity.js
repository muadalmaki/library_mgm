// Copyright (c) 2024, Muad almakki and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Projected Quantity"] = {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
        },
        {
            fieldname: "warehouse",
            label: __("Warehouse"),
            fieldtype: "Link",
            options: "Warehouse",
            get_query: () => {
                return {
                    filters: {
                        company: frappe.query_report.get_filter_value("company"),
                    },
                };
            },
        },
        {
            fieldname: "item_code",
            label: __("Item"),
            fieldtype: "Link",
            options: "Item",
            get_query: function () {
                return {
                    query: "erpnext.controllers.queries.item_query",
                };
            },
        },
        {
            fieldname: "item_group",
            label: __("Item Group"),
            fieldtype: "Link",
            options: "Item Group",
        },
        {
            fieldname: "brand",
            label: __("Brand"),
            fieldtype: "Link",
            options: "Brand",
        },
        {
            fieldname: "include_uom",
            label: __("Include UOM"),
            fieldtype: "Link",
            options: "UOM",
        },
    ],
    onload: function(report) {
        // Add a custom button with blue color directly on the report's page
        $(report.page.wrapper).append(`
            <button id="custom-report-button" class="btn btn-primary" style="background-color: #007bff; border-color: #007bff; color: white; position: absolute; top: 20px; right: 20px; z-index: 9999;">
                ${__('Show Details')}
            </button>
        `);

        // Add click event listener for the button
        $('#custom-report-button').on('click', function() {
            frappe.msgprint({
                title: __('Report Created By'),
                message: __('This report was created by Muad Nuri.'),
                indicator: 'blue',
            });
        });
    }
};

