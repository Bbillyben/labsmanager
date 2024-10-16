// {% load i18n %}
/*  Credit : Inventree https://github.com/inventree/InvenTree
* for the overall process of bootstraptable filter
*/
// {% include "status_codes.html" with label='build' options=BuildStatus.list %}

function getAvailableTableFilters(tableKey) {
    tableKey = tableKey.toLowerCase();
    // console.log("[getAvailableTableFilters] : "+tableKey)
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
            superior_name:{
                title: 'Responsible Name',
                description: 'Responsible Name',
            },
            status:{
                title : 'Employee Status',
                description: 'Employee Status Code',
                options:employee_status_codes,
            },
            current_status:{
                title : 'Current Employee Status',
                description: 'Employee Status Code',
                options:employee_status_codes,
            },
        };
    }
    if (tableKey.substring(0,8) == 'contract') {
        return {
            
            active: {
                type: 'bool',
                title: 'Active',
            },
            ongoing: {
                type: 'bool',
                title: 'Ongoing',
            },
            name: {
                title: 'Employee Name',
                description: 'Employee Name',
            },
            type:{
                title : 'Contract Type',
                options: contract_type_codes,
            },
            cont_status:{
                title : 'Contract Status',
                options: contract_status_codes,
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
            fundref:{
                title: 'Fund Ref'
            },
            stale: {
                type: 'bool',
                title: 'Is Stale',
            },
            

        };
    }
    if (tableKey == 'project_orga') {
        return {
            
            status: {
                type: 'bool',
                title: 'Active',
            },
            project_name: {
                title: 'Project Name',
                description: 'Project Name',
            }           

        };
    }
    if (tableKey.substring(0,8) == 'funditem') {
        return {
            fund_type:{
                title:'Type',
                description: 'general type',
                options: cost_type_codes,
            },
            available:{
                title:'Available Amount',
                description: 'minimum amount available',
            },
            active: {
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
            fundref:{
                title: 'Fund Ref'
            },
            stale: {
                type: 'bool',
                title: 'Is Stale',
            },
        };
        
    }

    if (tableKey == 'leave') {
        return {
            
            name: {
                title: 'Employee Name',
                description: 'Employee Name',
            },
            type:{
                title : 'Leave Type',
                description: 'Leave Type Status code',
                options:leave_type_codes,
            },
            start:{
                title: 'start date',
                type:'date'
            }
        };
    }
    if (tableKey == 'teams') {
        return {
            
            name: {
                title: 'Team Name',
                description: 'Team Name',
            },
            leader:{
                title : 'Leader Name',
                description: 'Team Leader name',
            },
            mate:{
                title: 'Team Mate Name'
            }
        };
    }
    if (tableKey.substring(0,6) == 'budget') {
        return {
            
            active: {
                type: 'bool',
                title: 'Active',
            },
            type: {
                title: 'Cost Type',
                options:cost_type_codes,
            },
            contract_type:{
                title : 'Contract Type',
                options: contract_type_codes,
            },
            emp_name: {
                title: 'Employee Name',
                description: 'Employee Name',
            },
            project_name: {
                title: 'Project Name',
                description: 'Project Name',
            },
            institution: {
                title: 'Institution',
                description: 'Institution Name',
                options: institution_codes,
            },
        };
    }
    if (tableKey.substring(0,7) == 'contrib') {
        return{
            active_contrib: {
                type: 'bool',
                title: 'Active',
            },
        }
    };

    // Finally, no matching key
    return {};
}