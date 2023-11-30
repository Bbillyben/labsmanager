// {% load i18n %}
/*  Credit : Inventree https://github.com/inventree/InvenTree
* for jQueryTable wrapper
* 
*/

function reloadtable(table) {
    $(table).bootstrapTable('refresh');
}





function convertQueryParameters(params, filters) {

    // Override the way that we ask the server to sort results
    // It seems bootstrap-table does not offer a "native" way to do this...
    if ('sort' in params) {
        var order = params['order'];

        var ordering = params['sort'] || null;

        if (ordering) {
            if (order == 'desc') {
                ordering = `-${ordering}`;
            }

            params['ordering'] = ordering;
        }

        delete params['sort'];
        delete params['order'];

    }

    for (var key in filters) {
        params[key] = filters[key];
    }

    if ('order' in filters) {
        params['order'] = filters['order'];
    }

    // Remove searchable[] array (generated by bootstrap-table)
    if ('searchable' in params) {
        delete params['searchable'];
    }

    if ('sortable' in params) {
        delete params['sortable'];
    }

    // If "original_search" parameter is provided, add it to the "search"
    if ('original_search' in params) {
        var search = params['search'] || '';

        var clean_search = sanitizeInputString(search + ' ' + params['original_search']);

        params['search'] = clean_search;

        delete params['original_search'];
    }

    return params;
}

/**
 * Return a standard list of export format options *
 */
 function exportFormatOptions() {
    return [
        {
            value: 'csv',
            display_name: 'CSV',
        },
        {
            value: 'tsv',
            display_name: 'TSV',
        },
        {
            value: 'xls',
            display_name: 'XLS',
        },
        {
            value: 'xlsx',
            display_name: 'XLSX',
        },
    ];
}

/**
 * Download data from a table, via the API.
 * This requires a number of conditions to be met:
 *
 * - The API endpoint supports data download (on the server side)
 * - The table is "flat" (does not support multi-level loading, etc)
 * - The table has been loaded using the inventreeTable() function, not bootstrapTable()
 *   (Refer to the "reloadTableFilters" function to see why!)
 */
 function downloadTableData(table, opts={}) {

    // Extract table configuration options
    var table_options = table.bootstrapTable('getOptions');
    

    var url = table_options.url;

    if (!url) {
        console.error('downloadTableData could not find "url" parameter.');
    }

    var query_params = table_options.query_params || {};

    url += '?';

    constructFormBody({}, {
        title: opts.title || 'Export Table Data',
        fields: {
            format: {
                label: 'Format',
                help_text: 'Select File Format',
                required: true,
                type: 'choice',
                value: 'csv',
                choices: exportFormatOptions(),
            }
        },
        onSubmit: function(fields, form_options) {
            var format = getFormFieldValue('format', fields['format'], form_options);

            // Hide the modal
            $(form_options.modal).modal('hide');

            for (const [key, value] of Object.entries(query_params)) {
                url += `${key}=${value}&`;
            }

            url += `export=${format}`;

            location.href = url;
        }
    });
}

/*
 * Reload a table which has already been made into a bootstrap table.
 * New filters can be optionally provided, to change the query params.
 */
function reloadTableFilters(table, filters) {

    // Simply perform a refresh
    if (filters == null) {
        table.bootstrapTable('refresh');
        return;
    }

    // More complex refresh with new filters supplied
    var options = table.bootstrapTable('getOptions');

    // Construct a new list of filters to use for the query
    var params = {};

    for (var k in filters) {
        params[k] = filters[k];
    }

    // Original query params will override
    if (options.original != null) {
        for (var key in options.original) {
            params[key] = options.original[key];
        }
    }

    // Store the total set of query params
    // This is necessary for the "downloadTableData" function to work
    options.query_params = params;

    options.queryParams = function(tableParams) {
        return convertQueryParameters(tableParams, params);
    };

    table.bootstrapTable('refreshOptions', options);
    table.bootstrapTable('refresh', filters);
}

function visibleColumnString(columns) {
    /* Generate a list of "visible" columns to save to file. */

    var fields = [];

    columns.forEach(function(column) {
        if (column.switchable && column.visible) {
            fields.push(column.field);
        }
    });

    return fields.join(',');
}

function labTableUpdate(eventName, table, options, playCallback=true){

    switch(eventName){

        case 'load-success.bs.table':
            if(options.callback && playCallback)options.callback();
            break;
        case "refresh.bs.table":
        case "search.bs.table":
        case "refresh.bs.table":
            if(options.callback)options.callback();
            break;
    }

    if(eventName!="post-body.bs.table")return;

   var defaults = {
        modalID:"#create-modal",
        modalContent:".modal-content",
        modalForm:".modal-content form",
    };
    settings = $.extend(defaults, options);

    $(table).find('.edit').each(function(){
        //console.log("edit_employee found :"+$(this).data("form-url"))
        $(this).labModalForm({
            modalID: settings.modalID,
            modalContent: settings.modalContent,
            modalForm: settings.modalForm,
            formURL: $(this).data("form-url"),
            addModalFormFunction: function(){reloadtable(table)},
            modal_title:"Edit",
        })
    })
    $(table).find('.delete').each(function(){
        $(this).labModalForm({
            modalID: settings.modalID,
            modalContent: settings.modalContent,
            modalForm: settings.modalForm,
            isDeleteForm: true,
            formURL: $(this).data("form-url"),
            addModalFormFunction: function(){reloadtable(table)},
            modal_title:"Delete",
        })
    })    
}
$.fn.labTable = function(options) {

    var table = this;

    var tableName = options.name || 'table';

    var varName = tableName + '-pagesize';

    // Pagingation options (can be server-side or client-side as specified by the caller)
    if (!options.disablePagination) {
        options.pagination = true;
        options.paginationVAlign = options.paginationVAlign || 'both';
        options.pageSize = options.pageSize || labLoad(varName, 25);
        options.pageList = [10, 25, 50, 100, 250, 'all'];
        options.totalField = 'count';
        options.dataField = 'results';

    } else {
        options.pagination = false;
    }

    // Extract query params
    var filters = options.queryParams || options.filters || {};

    options.escape = true;

    // Store the total set of query params
    options.query_params = filters;

    options.queryParams = function(params) {
        // Update the query parameters callback with the *new* filters
        return convertQueryParameters(params, filters);
    };

    options.rememberOrder = true;

    if (options.sortable == null) {
        options.sortable = true;
    }

    if (options.search == null) {
        options.search = true;
    }

    if (options.showColumns == null) {
        options.showColumns = true;
    }

    // Callback to save pagination data
    options.onPageChange = function(number, size) {
        labSave(varName, size);
    };

    // Callback when a column is changed
    options.onColumnSwitch = function() {

        var columns = table.bootstrapTable('getVisibleColumns');

        var text = visibleColumnString(columns);

        // Save visible columns
        labSave(`table_columns_${tableName}`, text);
    };

    options.onAll=function(e){labTableUpdate(e, table, options, options.playCallbackOnLoad)};

    // Standard options for all tables
    table.bootstrapTable(options);

    // Load visible column list from memory
    // Load visible column list
    var visibleColumns = labLoad(`table_columns_${tableName}`, null);

    // If a set of visible columns has been saved, load!
    if (visibleColumns) {
        var columns = visibleColumns.split(',');

        // Which columns are currently visible?
        var visible = table.bootstrapTable('getVisibleColumns');

        if (visible && Array.isArray(visible)) {
            visible.forEach(function(column) {

                // Visible field should *not* be visible! (hide it!)
                if (column.switchable && !columns.includes(column.field)) {
                    table.bootstrapTable('hideColumn', column.field);
                }
            });
        } else {
            console.error(`Could not get list of visible columns for table '${tableName}'`);
        }
    }


};


/*  --------------------------------------------------
                  Table Row Selection          
------------------------------------------------------- */
function makeTableRowSelect(row, className='select-row'){
    //console.log(row)
    if(!row)return;
    rows=$(row).closest('tbody');
    rows.find('tr').each(function(){$(this).removeClass(className)});
    $(row).addClass(className);    
}

function getRowOrderByProperty(selector, key, value) {
    var data = $(selector).bootstrapTable("getData");
    var result = [];
    data.filter(function (o, i) {
      if (o[key] === value) {
        result.push(i);
      }
    });
    return result;
  }


/*  --------------------------------------------------
                  Basic Tables cell formatter         
------------------------------------------------------- */

// --------------------Sytle
function styleAlignMiddle(value, row, index, field){
    response={
    //classes: 'text-nowrap another-class',
        css: {"text-align": "center"}
    }
      return response;
}


// -------------------- Formatter
function baseDateFormatter(value, row, index, field){
    if(value == null || value =="")return value
    d=new Date(value)
    if (d == "Invalid Date" )return value;
    return d.toLocaleDateString()
}

function basicBoolean(value, row, index, field){
    response = (value ? '<img src="/static/admin/img/icon-yes.svg" alt="True">' : '<img src="/static/admin/img/icon-no.svg" alt="False">');
    response += '<span style="display:none">'+ value+"</span>";
    return response
}


function quotityFormatter(value, row, index, field){
    if(isNaN(value))return '-'
    return quotityDisplay(value);
}

function quotityAlertFormatter(value, row, index, field){
    if( value == null || isNaN(value) ){
        return "-";
    }
    val = quotityDisplay(value)
    if(value > 1){
        return "<div class='warning-quotity'>"+val+"</div>";
    }else{
        return "<div class=''>"+val+"</div>";
    }
}

function moneyFormatter(value, row, index, field){
    return moneyDisplay(value);
}
function moneyFormatter_alert(value, row, index, field){
    response = '<span class="'+(value < 0 ? "text-danger":'')+'">';
    response+=moneyDisplay(value);
    response+='</span>';
    return response;
}

function availableFundItem_alert(value, row, index, field){
    response = moneyFormatter_alert(value, row, index, field);
    if(row.contract.length > 0){
        var cc = "";
        for (var i = 0; i < row.contract.length; i++) {
            if(cc.length>1)cc+="\n";
            cc+=row.contract[i].employee.user_name+' - '
            if(row.contract[i].quotity)cc+=quotityFormatter(row.contract[i].quotity)
            if(row.contract[i].contract_type)cc+=" - "+row.contract[i].contract_type
            if(row.contract[i].end_date)cc+=" - "+row.contract[i].end_date;
          }
        response+='<span class="availContract" tabindex="0" data-toggle="tooltip" data-placement="top" title="'+cc+'">'+row.contract.length+"</span>";
    }
    return response;
}

function moneyFocusFormatter(value, row, index, field){
    //console.log("[moneyFocusFormatter] custom data :"+this.custom_param)
    str = moneyFormatter(value, row, index, field)
    focusItem = row[this.custom_param]
    if(focusItem != undefined && focusItem != value){
        str += "<small> ("+moneyDisplay(focusItem)+") </small>"
    }
    return str

}

function employeeFormatter(value, row, index, field){

    if(!isIterable(value)){
        value=[{"employee":value}];
    }
    response = "";
    for (const item of value) {
        // console.log("item :"+JSON.stringify(item));
            if("employee" in item && item.employee!=null){
                tm ="<a href='/staff/employee/"+item.employee.pk+"'>"+item.employee.user_name+"</a>";
                response+= (response.length > 1 ? ', ' : '') + tm;
            }else{
                response +="-"
            }
            
      }
      return response;
}


function teamMateFormatter(value, row, index, field){
    
    if(!isIterable(value)){
        value=[{"employee":value, "is_active":value.is_active}];
    }
    response = "";
    for (const item of value) {
        //console.log("item :"+JSON.stringify(item));
        //if (item.employee.is_active == true){

            tm ="<a href='/staff/employee/"+item.employee.pk+"'>"+item.employee.user_name+"</a>";
            if(!item.is_active)tm +='<sup><img src="/static/admin/img/icon-no.svg" alt="False" style="width:1em;"></img></sup>'
            response+= (response.length > 1 ? ', ' : '') + tm;
        //}
      }
      return response;
}

function ParticipantFormatter(value, row, index, field){
    // console.log('ParticipantFormatter'+JSON.stringify(value))
    // console.log('ParticipantFormatter'+JSON.stringify(row))

    if(!isIterable(value)){
        value=[{"employee":value}];
    }
    response = "";
    value = value.sort(leaderSorter);
    for (const item of value) {
        //console.log("item :"+JSON.stringify(item));
        if (item.employee.is_active == true){

            tm ="<a href='/staff/employee/"+item.employee.pk+"'>"+item.employee.user_name;
            if(item.status == "l"){
                tm+= '<sup><i class="fas fa-crown icon-spaced" style="color: coral" title="team leader"></i></sup>';
            }else if(item.status == "cl"){
                tm+= '<sup><i class="fas fa-crown icon-spaced" style="color: cadetblue" title="team leader"></i></sup>';
            }
            tm+="</a>";
            response+= (response.length > 1 ? ', ' : '') + tm;
        }
      }
      return response;
}

function InstitutionParticipantFormatter(value, row, index, field){
    if(!isIterable(value)){
        value=[{"institution":value}];
    }
    response = "";
    value = value.sort(leaderSorter);
    for (const item of value) {
        //console.log("item :"+JSON.stringify(item));

            tm =""+item.institution.short_name;
            if(item.status == "c"){
                tm+= '<sup><i class="fas fa-star icon-spaced" style="color: coral" title="team leader"></i></sup>';
            }
            //tm+="</a>";
            response+= (response.length > 1 ? ', ' : '') + tm;
      }
      return response;


}


function ProjectFormatter(value, row, index, field){
    // console.log("ProjectFormatter :"+JSON.stringify(value))
    if(!isIterable(value)){
        value=[{"project":value}];
    }
    response = "";
    for (const item of value) {
        // console.log("item :"+JSON.stringify(item));

            tm ="<a href='/project/"+item.project.pk+"'>"+item.project.name;
            tm+="</a>";
            response+= (response.length > 1 ? ', ' : '') + tm;
      }
      return response;
}


function SingleFundFormatter(value, row, index, field){
    
    response = "";
    response +=value.funder.short_name;
    response+=" - "+value.institution.short_name;
    response+=" ("+value.ref;
    response+=" - "+moneyDisplay(value.amount)+")"
    
      return response;
}


function FundFormatter(value, row, index, field){
    

    if(!isIterable(value)){
        value=[value];
    }
    response = "<ul>";
    for (const item of value) {
        response +="<li>"+item.funder.short_name;
        response+=" - "+item.institution.short_name;
        response+=" ("+item.ref;
        response+=" - "+moneyDisplay(item.amount)+")"
        response+="</li>";
      }
      response += "</ul>";
      return response;
}


function FocusItemFormatter(value, row, index, field){
    // console.log("[FocusItemFormatter]")
    // console.log(JSON.stringify(row))
    response = value;
    if(row.type != undefined){
        type=row.type;
    }else if(row.cost_type != undefined){
        type=row.cost_type;
    }
    if(type!=undefined && !type.in_focus){
        response+='<sup class="out-focus"><small><i class="fas fa-eye-slash" title="Out of focus"></i></small></sup>'
    }

    return response;
    
}

function projectFormatterDirect(value, row, index, field){
    // console.log(value)
    // console.log(row)
    response = '<a href="/project/'+value.pk+'" >'+value.name+"</a>";
    return response;
}

function dueDatePassed(value, row, index, field){
    curr=new Date();
    valDate=Date.parse(value);
    //console.log('date test :'+(curr.getTime()>valDate));
    
    if(curr.getTime()>valDate){
        return '<span class="alert-danger">'+value+'</span>';
    }
    return value
}


function TeamFormatter(value, row, index, field){
    response =  '<span class="icon-right-cell"><a href="'+Urls['team_single'](row.pk)+'" title="/'+row.ipkd+'/"> '+value+'</a>';
    return response;
}


function leaveEmployeeFormatter(value, row, index, field){
    response =  '<a href="'+Urls['employee'](row.employee_pk)+'" title="/'+row.employee_pk+'/"> '+value+'</a>';
    return response;
}

function colorFormatter(value, row, index, field){
    response = "<span class='color-dot'style=' background-color:"+value+";'></span>"
    return response;
}   

function iconFormatter(value, row, index, field){
    response = "<i class='"+value.style+" fa-"+value.icon+"'></i>"
    return response;
}   


function m2mBaseFormatter(value, row, index, field){
    response=value.map(function(elem){
        return elem.name;
    }).join(", ");

    return response
}

function treeNameFormatter(value, row, index, field){
    response = ""
    for(i=0; i<row.ancestors_count; i++){
        if(i==0){response +="┝";}else{response +="┅";}
        response +="━";
        if(i==row.ancestors_count-1)response +=" "
    }
    response+=value
    return response
}
// --------------------     Basic Table Sorter    ------------------- // 

function nameSorter(fieldA, fieldB){
    //console.log('[activeSorter] '+JSON.stringify(fieldA)+" / "+JSON.stringify(fieldB)+" / "+JSON.stringify(q));
    A =  fieldA.first_name+" "+fieldA.last_name;
    B = fieldB.first_name+" "+fieldB.last_name;
    if (A <B) return -1;
      if (A > B) return 1;
      return 0;
  }
function projectNameSorter(fieldA, fieldB, q){
    //console.log('[projectNameSorter] '+JSON.stringify(fieldA)+" / "+JSON.stringify(fieldB)+" / "+JSON.stringify(q));
    A =  fieldA.name;
    B = fieldB.name;
    if (A <B) return -1;
      if (A > B) return 1;
      return 0;
  }
function leaderSorter(fA, fB){
    //console.log( "[leaderSorter] :"+fA.employee.user_name+"("+fA.status+")  "+fB.employee.user_name+"("+fB.status+")");
    A=fA.status;
    B=fB.status;
    if(A == "l" || A =="c")return -1;
    if(B == "l" || B =="c")return 1;
    if(A == "cl" && B!="l")return -1;
    if(B == "cl" && A!="l")return 1;
    if(!A && B) return -1;
    if(A && !B)return 1;
    return 0;
}