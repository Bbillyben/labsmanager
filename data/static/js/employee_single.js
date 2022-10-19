// ----------------------  Common  ------------------- //
function initEmployeeSingleView(user_id, employee_id){
    $('#employee_team_table').bootstrapTable();
    $('#employee_contract_table').bootstrapTable();
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
            dataUrl: '/api/employee/'+employee_id,
            dataElementId: '#employee_single_table',
            dataKey: 'table',
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
            dataElementId: '#employee_single_table',
            dataKey: 'table',
            addModalFormFunction: update_status,
        }
    })
    update_activ_btn();
}

// ----------------------  Employee  ------------------- //
function update_employee(){
    window.location.reload();
    update_activ_btn();
    
}
function update_activ_btn(){
    $('.user_action').click(function(){
        console.log('user_action clicl');

        data_action = $(this).data('action-type');
        item_pk= $(this).data('pk');
        user_id = JSON.parse(document.getElementById('user_id').textContent);
        urlAjax= $(this).data('url');
        console.log('data_action :'+data_action);
        console.log('item_pk :'+item_pk);
        console.log('user_id :'+user_id);
        csrftoken = getCookie('csrftoken');

        if (user_id == item_pk){
            return;
        }
        

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
    action += "<button class='icon edit_status_emp btn btn-success' data-form-url='/staff/status/"+row.pk+"/update/' ><i type = 'button' class='fas fa-edit'></i></button>";
    action += "<button class='icon delete_status_emp btn btn-danger ' data-form-url='/staff/status/"+row.pk+"/delete/' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}

// ----------------------  table Contract  ------------------- //

function quotityFormatter(value, row, index, field){
        return parseFloat(value*100).toFixed(0)+" %"
}


// ----------------------  table Team  ------------------- //
function teamMateFormatter(value, row, index, field){
    response = "";
    for (const item of value) {
        if (item.end_date == null){
          response+= (response.length > 1 ? ', ' : '') + item.employee.user_name
        }
      }
      return response;
}






function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}