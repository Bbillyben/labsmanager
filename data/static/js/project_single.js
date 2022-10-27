
var user_id = 0;
var project_id = 0;

function initProjectSingleView(user_idA, project_idA){
        
    let user_id = user_idA;
    let project_id = project_idA;
    //console.log("initProjectSingleView :"+project_id)


    // MOdal for Project edition
    $('#edit-project').modalForm({
        modalID: "#create-modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: '/project/ajax/'+project_id+'/udpate',
        isDeleteForm: false,
        errorClass: ".form-validation-warning",
        asyncUpdate: true,
        asyncSettings: {
            directUpdate: true,
            closeOnSubmit: true,
            successMessage: "Employee Updated",
            dataUrl: "/staff/ajax/"+project_id+"/activ",
            dataElementId: '#employee_single_table',
            dataKey: '0',
            addModalFormFunction: update_project,
        }
    })

    $('#project_participant_table').bootstrapTable({
        onLoadSuccess: function(){ updateParticipantBtnHandler();},
        onSearch: function(){ updateParticipantBtnHandler();},
        onSort: function(){  updateParticipantBtnHandler();},
        onToggle: function(){ updateParticipantBtnHandler();},
        onPageChange: function(){ updateParticipantBtnHandler();},
    });


    $('#add_participant').modalForm({
        modalID: "#create-modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: '/project/ajax/'+project_id+'/participant/add',
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


    $('#add_fund_temp').modalForm({
        modalID: "#create-modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: '/fund/ajax/add/' + $("#add_fund_temp").data("projectpk"),
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
            addModalFormFunction: updateFund,
        }
    });


    $('#project_contract_table').bootstrapTable({
        onLoadSuccess: function(){ updateContractBtnHandler();},
        onSearch: function(){ updateContractBtnHandler();},
        onSort: function(){  updateContractBtnHandler();},
        onToggle: function(){ updateFundBtupdateContractBtnHandlernHandler();},
        onPageChange: function(){ updateContractBtnHandler();},
    });

    $('#add_contract').modalForm({
        modalID: "#create-modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: '/expense/ajax/contract/add/project/'+project_id,
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


    update_project();
    

}


// ----------------------  Project Main  ------------------- //
function updateMainButton(){
    $('.project_action').click(function(){

        data_action = $(this).data('action-type');
        item_pk= $(this).data('pk');
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
                update_project();
            },
            error:function( err )
            {
                 $("body").html(err.responseText)
                console.log(JSON.stringify(err));
            }
        })
    });

    

}
function update_project(){
    //window.location.reload();
    //console.log("update_project called :"+project_id);
    csrftoken = getCookie('csrftoken');
    $.ajax({
        type:"POST",
        url: "/project/ajax/"+project_id+"/resume",
        data:{
                pk:project_id,
                csrfmiddlewaretoken: csrftoken,
        },
        success: function( data )
        {
            $('#project_desc_table').html(data);
            updateMainButton();
            
        },
        error:function( err )
        {
             $("body").html(err.responseText)
            //console.log(JSON.stringify(err));
        }
    })    
}


// ----------------------  Participant  ------------------- //

function updateParticipant(){
    $('#project_participant_table').bootstrapTable('refresh');
}
function updateParticipantBtnHandler(){
    $(".edit_participant").each(function () {
        console.log("updateProjectTable :"+this);
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

function adminActionParticipant(value, row, index, field){
    action = "<span class='icon-left-cell btn-group'>";
    if(this.canChange=="True")action += "<button class='icon edit_participant btn btn-success' data-form-url='/project/ajax/participant/"+row.pk+"/udpate' ><i type = 'button' class='fas fa-edit'></i></button>";
    if(this.canDelete=="True")action += "<button class='icon delete_participant btn btn-danger ' data-form-url='/project/ajax/participant/"+row.pk+"/delete' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}

// ----------------------  Fund & Fund Item  ------------------- //







// --------------------- Contract Table