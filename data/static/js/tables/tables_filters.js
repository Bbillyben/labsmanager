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
    if (tableKey == 'contract') {
        return {
            
            active: {
                type: 'bool',
                title: 'Active',
            },
            name: {
                title: 'Employee Name',
                description: 'Employee Name',
            },
            type:{
                title : 'Contract Type',
                options: contract_type_codes,
            },
            project_name: {
                title: 'Project Name',
                description: 'Project Name',
            },
            funder: {
                title: 'Funder',
                options: fund_institution_codes,
            },
            institution_name: {
                title: 'Institution Name',
                description: 'Institution Name',
                options: institution_codes,
            },
            stale: {
                type: 'bool',
                title: 'Is Stale',
            },

        };
    
    }
    if (tableKey == 'project') {
        return {
            
            status: {
                type: 'bool',
                title: 'Active',
            },
            project_name: {
                title: 'Project Name',
                description: 'Project Name',
            },
            participant_name: {
                title: 'Participant Name',
                description: 'Participant Name',
            },
            institution_name: {
                title: 'Institution Name',
                description: 'Institution Name',
                options: institution_codes,
            },
            funder: {
                title: 'Funder',
                options: fund_institution_codes,
            },
            stale: {
                type: 'bool',
                title: 'Is Stale',
            },
            

        };
    }


    // Finally, no matching key
    return {};
}