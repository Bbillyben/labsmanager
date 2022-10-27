// ----------------------  Common  ------------------- //
employee_id= 0;
user_id= 0;

function initEmployeeSingleView(user_idA, employee_idA){
    employee_id=employee_idA;
    user_id = user_idA;
    

    $('#employee_team_table').bootstrapTable();
    $('#employee_contract_table').bootstrapTable({
        onLoadSuccess: function(){ updateContractBtnHandler();},
        onSearch: function(){ updateContractBtnHandler();},
        onSort: function(){  updateContractBtnHandler();},
        onToggle: function(){ updateContractBtnHandler();},
        onPageChange: function(){ updateContractBtnHandler();},
    });

    $('#employee_project_table').bootstrapTable({
        onLoadSuccess: function(){ updateParticipantBtnHandler();},
        onSearch: function(){ updateParticipantBtnHandler();},
        onSort: function(){  updateParticipantBtnHandler();},
        onToggle: function(){ updateParticipantBtnHandler();},
        onPageChange: function(){ updateParticipantBtnHandler();},
    });
    
    $('#employee_status_table').bootstrapTable({
        onLoadSuccess: function(){ update_status_btn();},
        onSearch: function(){ update_status_btn();},
        onSort: function(){  update_status_btn();},
        onToggle: function(){ update_status_btn();},
        onPageChange: function(){ update_status_btn();},
    });
    // MOdal for employee edition
    $('#edit-employee').modalForm({
        modalID: "#create-modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: '/staff/employee/'+employee_id+'/udpate',
        isDeleteForm: false,
        errorClass: ".form-validation-warning",
        asyncUpdate: true,
        asyncSettings: {
            directUpdate: true,
            closeOnSubmit: true,
            successMessage: "Employee Updated",
            dataUrl: "/staff/ajax/"+employee_id+"/activ",
            dataElementId: '#employee_single_table',
            dataKey: '0',
            addModalFormFunction: update_employee,
        }
    });

    $('#add-status').modalForm({
        modalID: "#create-modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: '/staff/employee/'+employee_id+'/status/add/',
        isDeleteForm: false,
        errorClass: ".form-validation-warning",
        asyncUpdate: true,
        asyncSettings: {
            directUpdate: true,
            closeOnSubmit: true,
            successMessage: "Employee Updated",
            dataUrl: '/api/employee/'+employee_id,
            dataElementId: '#employee_dec_table',
            dataKey: 'table',
            addModalFormFunction: update_status,
        }
    })

    $('#add_project').modalForm({
        modalID: "#create-modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: '/project/ajax/participant/add/'+employee_id,
        isDeleteForm: false,
        errorClass: ".form-validation-warning",
        asyncUpdate: true,
        asyncSettings: {
            directUpdate: true,
            closeOnSubmit: true,
            successMessage: "Employee Updated",
            dataUrl: '/api/employee/',
            dataElementId: '#employee_dec_table',
            dataKey: 'table',
            addModalFormFunction: updateParticipant,
        }
    })

    $('#add_contract').modalForm({
        modalID: "#create-modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: '/expense/ajax/contract/add/employee/'+employee_id,
        isDeleteForm: false,
        errorClass: ".form-validation-warning",
        asyncUpdate: true,
        asyncSettings: {
            directUpdate: true,
            closeOnSubmit: true,
            successMessage: "Employee Updated",
            dataUrl: '/api/employee/',
            dataElementId: '#employee_dec_table',
            dataKey: 'table',
            addModalFormFunction: updateContract,
        }
    })

    update_employee();
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
}

// ----------------------  Status  ------------------- //
function update_status(){
    $('#employee_status_table').bootstrapTable('refresh');
    update_status_btn();

}

function update_status_btn(){
    $(".edit_status_emp").each(function () {
        $(this).modalForm({
            modalID: "#create-modal",
            modalContent: ".modal-content",
            modalForm: ".modal-content form",
            formURL: $(this).data("form-url"),
            isDeleteForm: false,
            errorClass: ".form-validation-warning",
            asyncUpdate: true,
            asyncSettings: {
                directUpdate: true,
                closeOnSubmit: true,
                successMessage: "Employee Updated",
                dataUrl: '/api/employee/',
                dataElementId: '#employee_main_table',
                dataKey: 'table',
                addModalFormFunction: update_status,
            }
        });
    });

    $(".delete_status_emp").each(function () {
        $(this).modalForm({
            modalID: "#create-modal",
            modalContent: ".modal-content",
            modalForm: ".modal-content form",
            formURL: $(this).data("form-url"),
            isDeleteForm: true,
            errorClass: ".form-validation-warning",
            asyncUpdate: true,
            asyncSettings: {
                directUpdate: true,
                closeOnSubmit: true,
                successMessage: "Employee Updated",
                dataUrl: '/api/employee/',
                dataElementId: '#employee_main_table',
                dataKey: 'table',
                addModalFormFunction: update_status,
            }
        });
    });
}

function empStatusFormatter(value, row, index, field){
    //console.log('statusFormatter : '+JSON.stringify(value)+" - row : "+JSON.stringify(row) + "  - index :"+index+ " - fiels :"+field+"  # allow :"+this.allow);
    action = "<span class='icon-left-cell btn-group'>";
    if(this.canChange=='True')action += "<button class='icon edit_status_emp btn btn-success' data-form-url='/staff/status/"+row.pk+"/update/' ><i type = 'button' class='fas fa-edit'></i></button>";
    if(this.canDelete=='True')action += "<button class='icon delete_status_emp btn btn-danger ' data-form-url='/staff/status/"+row.pk+"/delete/' ><i type = 'button' class='fas fa-trash'></i></button>";
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
    if(this.canChange=="True")action += "<button class='icon edit_participant btn btn-success' data-form-url='/project/ajax/participant/"+row.pk+"/udpate' ><i type = 'button' class='fas fa-edit'></i></button>";
    if(this.canDelete=="True")action += "<button class='icon delete_participant btn btn-danger ' data-form-url='/project/ajax/participant/"+row.pk+"/delete' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}
function updateParticipantBtnHandler(){
    $(".edit_participant").each(function () {
        //console.log("updateProjectTable :"+this);
        $(this).modalForm({
            modalID: "#create-modal",
            modalContent: ".modal-content",
            modalForm: ".modal-content form",
            formURL: $(this).data("form-url"),
            isDeleteForm: false,
            errorClass: ".form-validation-warning",
            asyncUpdate: true,
            asyncSettings: {
                directUpdate: true,
                closeOnSubmit: true,
                successMessage: "Employee Updated",
                dataUrl: '/api/employee/',
                dataElementId: '#employee_main_table',
                dataKey: 'table',
                addModalFormFunction: updateParticipant,
            }
        });
    });
    $(".delete_participant").each(function () {
        $(this).modalForm({
            modalID: "#create-modal",
            modalContent: ".modal-content",
            modalForm: ".modal-content form",
            formURL: $(this).data("form-url"),
            isDeleteForm: true,
            errorClass: ".form-validation-warning",
            asyncUpdate: true,
            asyncSettings: {
                directUpdate: true,
                closeOnSubmit: true,
                successMessage: "Employee Updated",
                dataUrl: '/api/employee/',
                dataElementId: '#employee_main_table',
                dataKey: 'table',
                addModalFormFunction: updateParticipant,
            }
        });
    });
}
// ----------------------  table Contract  ------------------- //







// ----------------------  table Team  ------------------- //


