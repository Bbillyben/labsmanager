var callbackFund;
var callbackFundItem;

var fundPk=0;
var csrftoken=0;

function initializeFundTable(callback_fund=null, callback_funditem=null){
    callbackFund=callback_fund;
    callbackFundItem=callback_funditem;

    var options={
        url:$('#project_fund_table').data("url"),
        name:'fund',
        disablePagination:true,
        search:false,
        showColumns:false,
        onClickRow:fundRowclick, 
        callback:updateFundSelection,

        
    }

    $('#project_fund_table').labTable(options);

}
function fundRowclick( row, element, field){
    fundPk=row["pk"];
    csrftoken = getCookie('csrftoken');
    // fund overview
    if($('#fund_overview').exists())updateFundOverviewTableAjax(fundPk, csrftoken);
    // Fund item
    if($('#fund_item_detail').exists())updateFundItemTableAjax(fundPk, csrftoken);
    if($('#fund_expense_timepoint_detail').exists())updateFundExpenseTimepointTableAjax(fundPk, csrftoken);
    if($('#fund_item_expense').exists())updateExpenseTableAjax(fundPk, csrftoken);
    makeTableRowSelect(element);
}
function updateFundSelection(){
    if(fundPk!=0){
        elt=getRowOrderByProperty('#project_fund_table', 'pk', fundPk);
        if (elt && elt[0]){
            makeTableRowSelect($('#project_fund_table tr').eq(elt[0]+1))
        }
    }
}
function updateFund(){
    $('#project_fund_table').bootstrapTable('refresh');
    if(callbackFund!=null)callbackFund();
}
function updateFullFund(){
    $('#project_fund_table').bootstrapTable('refresh');
    $('#project_fund_item_table').bootstrapTable('refresh');
    //$('#project_expense_timepoint_table').bootstrapTable('refresh');
    //$('#project_expense_table').bootstrapTable('refresh');
    updateFundOverviewTableAjax(fundPk, csrftoken);
    if(callbackFundItem!=null)callbackFundItem();
}
function updageGlobalFund(){
    updateFullFund();
    $('#project_expense_timepoint_table').bootstrapTable('refresh');
}
function updateSubTables(){
    $('#project_fund_table').bootstrapTable('refresh');
    $('#project_fund_item_table').bootstrapTable('refresh');
    $('#project_expense_timepoint_table').bootstrapTable('refresh');
}
function updateAllSubTables(){
    updateSubTables();
    $('#project_expense_table').bootstrapTable('refresh');
}

function adminActionFund(value, row, index, field){
    action = "<span class='icon-left-cell btn-group'>";
    if(this.isStaff=='True')action += "<a href='/admin/fund/fund/"+row.pk+"/change/'><button class='icon admin_btn btn btn-primary'><i type = 'button' class='fas fa-shield-halved'></i></button></a>"
    if(this.canChange=='True' || row.has_perm==true)action += "<button class='icon edit btn btn-success' data-form-url='/fund/ajax/"+row.pk+"/update' ><i type = 'button' class='fas fa-edit'></i></button>";
    //action += "<button class='icon show_fund btn btn-secondary' data-fund='"+row.pk+"' ><i type = 'button' class='fas fa-toolbox'></i></button>";
    if(this.canDelete=='True')action += "<button class='icon delete btn btn-danger ' data-form-url='/fund/ajax/"+row.pk+"/delete' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}
function adminActionFundItem(value, row, index, field){
    action = "<span class='icon-left-cell btn-group'>";
    if(this.canChange=='True')action += "<button class='icon edit btn btn-success' data-form-url='/fund/ajax/funditem/"+row.pk+"/update' ><i type = 'button' class='fas fa-edit'></i></button>";
    if(this.canDelete=='True' || row.has_perm==true )action += "<button class='icon delete btn btn-danger ' data-form-url='/fund/ajax/funditem/"+row.pk+"/delete' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}
function adminActionExpensePointdItem(value, row, index, field){
    action = "<span class='icon-left-cell btn-group'>";
    if(this.canChange=='True')action += "<button class='icon edit btn btn-success' data-form-url='/fund/ajax/expense_timepoint/"+row.pk+"/update' ><i type = 'button' class='fas fa-edit'></i></button>";
    if(this.canDelete=='True' || row.has_perm==true)action += "<button class='icon delete btn btn-danger ' data-form-url='/fund/ajax/expense_timepoint/"+row.pk+"/delete' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}

function adminActionExpenseItem(value, row, index, field){
    action = "<span class='icon-left-cell btn-group'>";
    if(this.canChange=='True' || row.has_perm==true)action += "<button class='icon edit btn btn-success' data-form-url='"+Urls['update_expense'](row.pk)+"' data-model='"+row.class_type+"'><i type = 'button' class='fas fa-edit'></i></button>";
    if(this.canDelete=='True')action += "<button class='icon delete btn btn-danger ' data-form-url='"+Urls['delete_expense'](row.pk)+"'><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}
function expense_list_contractItem(value, row, index, field){
    // console.log('expense_list_contractItem *************************')
    // console.log(' - value : '+JSON.stringify(value))
    // console.log(' - row : '+JSON.stringify(row))
    if ( value == null){
        return "-"
    }
    response = ""
    response += "<strong>"+value.employee.user_name+'</strong>';
    response += '<small><i>  '+value.contract_type+' - '+value.start_date+" # "+value.end_date+"</i></small>"
    return response;
}


function updateFundItem(){
    var options={
        url:$('#project_fund_item_table').data("url"),
        name:'fund_item',
        disablePagination:true,
        search:false,
        showColumns:false,
        callback:updateFund,
        playCallbackOnLoad:false,
        
    }
    $('#project_fund_item_table').labTable(options)
    
    $('#add_fund_item_temp').labModalForm({
            formURL: '/fund/ajax/funditem/add/' + $("#add_fund_item_temp").attr("data-fundPk"),
            addModalFormFunction: updateFullFund,
            modal_title:"Add",
        })
}

function updateExpenseTimepoint(){
    var options={
        url:$('#project_expense_timepoint_table').data("url"),
        name:'expense_timepoint',
        disablePagination:true,
        search:false,
        showColumns:false,
        callback:updateFullFund,
        playCallbackOnLoad:false,
        
    }

    $('#project_expense_timepoint_table').labTable(options)
    $('#add_expense_timepoint').labModalForm({
        formURL: '/fund/ajax/expense_timepoint/add/' + $("#add_expense_timepoint").attr("data-fundPk"),
        addModalFormFunction: updageGlobalFund,
        modal_title:"Add",
    })
}

function updateExpenseList(){
    var options={
        url:$('#project_expense_table').data("url"),
        name:'expense_list',
        disablePagination:true,
        search:false,
        showColumns:false,
        callback:updateSubTables,
        playCallbackOnLoad:false,
        
    }
    $('#project_expense_table').labTable(options)
    
    $('#add_expense').labModalForm({
            formURL: Urls["add_expense"]( $("#add_expense").attr("data-fundPk")),
            addModalFormFunction: updateAllSubTables,
            modal_title:"Add",
        })
    $('#sync_expense').labModalForm({
        formURL: Urls["fund_expense_sync"]( $("#add_expense").attr("data-fundPk")),
        addModalFormFunction: updateSubTables,
        modal_title:"Sync",
    })
}
// AJAX Function to update related tables
function updateFundItemTableAjax(fundPk, csrftoken){
    $.ajax({
        type:"GET",
        url: "/fund/ajax/"+fundPk+"/items/", 
        // data:{
        //         pk:fundPk,
        //         csrfmiddlewaretoken: csrftoken,
        // },
        success: function( data )
        {
            $('#fund_item_detail').html(data);
            updateFundItem();                    
        },
        error:function( err )
        {
            $("body").html(err.responseText)
            //console.log(JSON.stringify(err));
        }
    }) 
}
function updateFundOverviewTableAjax(fundPk, csrftoken){
    $.ajax({
        type:"GET",
        url: "/fund/"+fundPk+"/fundoverview/", 
        // data:{
        //         pk:fundPk,
        //         csrfmiddlewaretoken: csrftoken,
        // },
        success: function( data )
        {
            $('#fund_overview').html(data);
            updateFundItem();                    
        },
        error:function( err )
        {
            $("body").html(err.responseText)
            //console.log(JSON.stringify(err));
        }
    }) 
}
function updateFundExpenseTimepointTableAjax(fundPk, csrftoken){
    $.ajax({
        type:"GET",
        url: "/fund/"+fundPk+"/expense_timepoint/", 
        // data:{
        //         pk:fundPk,
        //         csrfmiddlewaretoken: csrftoken,
        // },
        success: function( data )
        {
            $('#fund_expense_timepoint_detail').html(data);
            updateExpenseTimepoint();                    
        },
        error:function( err )
        {
            $("body").html(err.responseText)
            //console.log(JSON.stringify(err));
        }
    }) 
}

function updateExpenseTableAjax(fundPk, csrftoken){
    $.ajax({
        type:"GET",
        url: "/fund/"+fundPk+"/expense/", 
        // data:{
        //         pk:fundPk,
        //         csrfmiddlewaretoken: csrftoken,
        // },
        success: function( data )
        {
            $('#fund_item_expense').html(data);
            updateExpenseList();                    
        },
        error:function( err )
        {
            $("body").html(err.responseText)
            //console.log(JSON.stringify(err));
        }
    }) 
}

