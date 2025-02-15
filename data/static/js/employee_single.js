// ----------------------  Common  ------------------- //
employee_id= 0;
user_id= 0;

// initi function called on panel loading
function initEmployeeProjectTable(){
    var options_part={
        callback:update_employee,
        url:$('#employee_project_table').data("url"),
        name:'participant',
        disablePagination:true,
        search:false,
        showColumns:false,
    }
    $('#employee_project_table').labTable(options_part);
}

function initEmployeeLeaveTable(){
    var filters = loadTableFilters('leave');
    var filterOption={
        download:true,
    }
    var options={
        queryParams: filters,
        name:'leave',        
    }
    setupFilterList('leave', $('#employee_leave_table'), '#filter-list-leave',filterOption);
    $('#employee_leave_table').labTable(options);
    initEmployeeCalendar();
}

function initEmployeeSingleView(user_idA, employee_idA){
    employee_id=employee_idA;
    user_id = user_idA;

    var options_status={
        url:$('#employee_status_table').data("url"),
        name:'status',
        disablePagination:true,
        search:false,
        showColumns:false,
    }
    $('#employee_status_table').labTable(options_status);

    // for superior table
    var options_superior={
        url:$('#employee_superior_table').data("url"),
        name:'surperior',
        disablePagination:true,
        search:false,
        showColumns:false,
    }
    $('#employee_superior_table').labTable(options_superior);
    // for subodrinate table
    var options_subordinate={
        url:$('#employee_subordinate_table').data("url"),
        name:'subordinate',
        disablePagination:true,
        search:false,
        showColumns:false,
    }
    $('#employee_subordinate_table').labTable(options_subordinate);
    // MOdal for employee edition
    $('#edit-employee').labModalForm({
        formURL: '/staff/employee/'+employee_id+'/udpate',
        addModalFormFunction: update_employee,
        modal_title:"Edit Employee",
    })

    $('#add-status').labModalForm({
        formURL: '/staff/employee/'+employee_id+'/status/add/',
        addModalFormFunction: update_status,
        modal_title:"Add Status",
    })

    $('#add-superior').labModalForm({
        formURL:  Urls['create_superior'](employee_id),
        addModalFormFunction: function(){$('#employee_superior_table').bootstrapTable('refresh');},
        modal_title:"Add Superior",
    })
    $('#add-subordinate').labModalForm({
        formURL:  Urls['create_subordinate'](employee_id),
        addModalFormFunction: function(){$('#employee_subordinate_table').bootstrapTable('refresh');},
        modal_title:"Add Subordinate",
    })

    $('#add_project').labModalForm({
        formURL:  '/project/ajax/participant/add/'+employee_id,
        addModalFormFunction: updateParticipant,
        modal_title:"Add Project",
    })

    $('#add_contract').labModalForm({
        formURL: '/expense/ajax/contract/add/employee/'+employee_id,
        addModalFormFunction: updateContract,
        modal_title:"Add Contract",
    })

    $('#add_leave').labModalForm({
        formURL:'/calendar/add/employee/'+employee_id+"/",
        addModalFormFunction: updateLeave,
        modal_title:"Add Leave",
    })
    $('#export_word').labModalForm({
        formURL: Urls['employee_report_generate'](employee_id),
        asyncSettings: {directUpdate:true,closeOnSubmit:true,},
        modal_title:"Export Word",
    })
    $('#export_pdf').labModalForm({
        formURL: Urls['employee_pdf_report_generate'](employee_id),
        asyncSettings: {directUpdate:true,closeOnSubmit:true,},
        modal_title:"Export PDF",
    })
    
    $('#show_emp_chart').labModal({
        templateURL: Urls['employee_org_chart_modal'](employee_id),
        modal_title:"Employee Organisation",
    })

    update_employee();
    update_employee_info();
    
    
    //updateLeaveBtnHandler();
}


// for calendar
function initEmployeeCalendar(){
    var canMod=USER_PERMS.includes("leave.change_leave") || USER_PERMS.includes("is_staff") || USER_PERMS.includes("can_edit");
    var option={
        selectable:canMod,
        editable:canMod,
        initialView:"dayGridMonth",
        extraParams:{employee:employee_id},
        eventCallback: function(){ $('#employee_leave_table').bootstrapTable('refresh')},
        cal_type:'employee',
        headerToolbar:{
            left: 'prev,next today datePickerButton',
            center: 'title',
            right: 'dayGridMonth,dayGridWeek,listWeek,timelineYearCustom'
        },
    }
    const view = localStorage.getItem(`labsmanager-calendar-view_employee`);
    if (view){
        option.initialView = view
    }
    calendar = $('#calendar-employee-box').lab_calendar_employee(option);
    

}

// ----------------------  Employee  ------------------- //
function update_employee(){
    //window.location.reload();
    csrftoken = getCookie('csrftoken');
    $.ajax({
        type:"POST",
        url: "/staff/ajax/"+employee_id+"/activ",
        data:{
                pk:employee_id,
                csrfmiddlewaretoken: csrftoken,
        },
        success: function( data )
        {
            $('#employee_dec_table').html(data);
            update_activ_btn();
        },
        error:function( err )
        {
             $("body").html(err.responseText)
            //console.log(JSON.stringify(err));
        }
    })    
}

function update_employee_info(){
    //window.location.reload();
    csrftoken = getCookie('csrftoken');
    $.ajax({
        type:"POST",
        url: Urls['employee_info_table'](employee_id),
        data:{
                pk:employee_id,
                csrfmiddlewaretoken: csrftoken,
        },
        success: function( data )
        {
            $('#employee_info_table').html(data);
            update_info_btn();
        },
        error:function( err )
        {
             $("body").html(err.responseText)
            //console.log(JSON.stringify(err));
        }
    })    
}


function update_activ_btn(){
    $('.user_action').click(function(){

        data_action = $(this).data('action-type');
        item_pk= $(this).data('pk');
        user_id = JSON.parse(document.getElementById('user_id').textContent);
        urlAjax= $(this).data('url');
        csrftoken = getCookie('csrftoken');
       

        $.ajax({
            type:"POST",
            url: urlAjax,
            data:{
                    action_type: data_action,
                    pk:item_pk,
                    csrfmiddlewaretoken: csrftoken,
            },
            success: function( data )
            {
                update_employee();
            },
            error:function( err )
            {
                 $("body").html(err.responseText)
                //console.log(JSON.stringify(err));
            }
        })
    });
    $("#employee_single_table .edit").each(function () {
        $(this).labModalForm({
            formURL: $(this).data("form-url"),
            addModalFormFunction: update_employee,
            modal_title:"Update",
        })
    });
}

// ----------------------  Status  ------------------- //
function update_status(){
    $('#employee_status_table').bootstrapTable('refresh');

}


function update_info_btn(){
    $(".update_info").each(function () {
        $(this).labModalForm({
            formURL: $(this).data("form-url"),
            addModalFormFunction: update_employee_info,
            modal_title:"Update Info",
        })
    });
    $(".delete_info").each(function () {
        $(this).labModalForm({
            formURL: $(this).data("form-url"),
            isDeleteForm: true,
            addModalFormFunction: update_employee_info,
            modal_title:"Delete Info",
        })
    });
        $('#add-info-gen').labModalForm({
        formURL:  Urls['create_info_employee'](employee_id),
        addModalFormFunction: update_employee_info,
        modal_title:"Add Info",
    })
}
function empStatusFormatter(value, row, index, field){
    //console.log('statusFormatter : '+JSON.stringify(value)+" - row : "+JSON.stringify(row) + "  - index :"+index+ " - fiels :"+field+"  # allow :"+this.allow);
    action = "<span class='icon-left-cell btn-group'>";
    if(this.canChange=='True')action += "<button class='icon edit btn btn-success' data-form-url='/staff/status/"+row.pk+"/update/' ><i type = 'button' class='fas fa-edit'></i></button>";
    if(this.canDelete=='True')action += "<button class='icon delete btn btn-danger ' data-form-url='/staff/status/"+row.pk+"/delete/' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}

function empActionSsuperiorFormatter(value, row, index, field){
    //console.log('statusFormatter : '+JSON.stringify(value)+" - row : "+JSON.stringify(row) + "  - index :"+index+ " - fiels :"+field+"  # allow :"+this.allow);
    action = "<span class='icon-left-cell btn-group'>";
    if(this.canChange=='True' || row.has_perm == true)action += "<button class='icon edit btn btn-success' data-form-url='"+Urls['update_superior'](row.pk)+"'' ><i type = 'button' class='fas fa-edit'></i></button>";
    if(this.canDelete=='True')action += "<button class='icon delete btn btn-danger ' data-form-url='"+Urls['delete_superior'](row.pk)+"' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}

// ----------------------  table Project  ------------------- //
function updateParticipant(){
    $('#employee_project_table').bootstrapTable('refresh');
    update_employee();
}
function adminActionParticipant(value, row, index, field){
    //console.log(JSON.stringify(row));
    action = "<span class='icon-left-cell btn-group'>";
    if(this.canChange=="True" || row.has_perm == true)action += "<button class='icon edit btn btn-success' data-form-url='/project/ajax/participant/"+row.pk+"/udpate' ><i type = 'button' class='fas fa-edit'></i></button>";
    if(this.canDelete=="True")action += "<button class='icon delete btn btn-danger ' data-form-url='/project/ajax/participant/"+row.pk+"/delete' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}

// ----------------------  table Leave  ------------------- //

function updateLeave(){
    $('#employee_leave_table').bootstrapTable('refresh');
    calendar.refetchEvents();
    //updateLeaveBtnHandler();
}

function adminActionLeave(value, row, index, field){
    //console.log(JSON.stringify(row));
    action = "<span class='icon-left-cell btn-group'>";
    if(this.isStaff=='True')action += "<a href='/admin/leave/leave/"+row.pk+"/change/'><button class='icon admin_btn btn btn-primary'><i type = 'button' class='fas fa-shield-halved'></i></button></a>"

    if(this.canChange=="True")action += "<button class='icon edit btn btn-success' data-form-url='/calendar/update/"+row.pk+"/' ><i type = 'button' class='fas fa-edit'></i></button>";
    
    if(this.canDelete=="True")action += "<button class='icon delete btn btn-danger ' data-form-url='/calendar/delete/"+row.pk+"/' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}



