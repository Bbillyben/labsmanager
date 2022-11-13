// {% load i18n %}
/* globals
    global_settings
*/

/* exported
    buildStatusDisplay,
    getAvailableTableFilters,
    purchaseOrderStatusDisplay,
    salesOrderStatusDisplay,
    stockHistoryStatusDisplay,
    stockStatusDisplay,
    
*/
// {% include "status_codes.html" with label='build' options=BuildStatus.list %}

function getAvailableTableFilters(tableKey) {

    tableKey = tableKey.toLowerCase();


    // Filters for Bill of Materials table
    if (tableKey == 'employee') {
        return {
            
            active: {
                type: 'bool',
                title: 'Active',
            },
            name: {
                title: 'Employee Name',
                description: 'Employee Name',
            },
            status:{
                title : 'Employee Status',
                description: 'Employee Status Code',
                options:employee_status_codes,
            }
        };
    }


    // Finally, no matching key
    return {};
}