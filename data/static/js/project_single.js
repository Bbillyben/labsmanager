
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

    $('#project_fund_table').bootstrapTable({
        onLoadSuccess: function(){ updateFundBtnHandler();},
        onSearch: function(){ updateFundBtnHandler();},
        onSort: function(){  updateFundBtnHandler();},
        onToggle: function(){ updateFundBtnHandler();},
        onPageChange: function(){ updateFundBtnHandler();},
    });


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
    action += "<button class='icon edit_participant btn btn-success' data-form-url='/project/ajax/participant/"+row.pk+"/udpate' ><i type = 'button' class='fas fa-edit'></i></button>";
    action += "<button class='icon delete_participant btn btn-danger ' data-form-url='/project/ajax/participant/"+row.pk+"/delete' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}

// ----------------------  Fund & Fund Item  ------------------- //

function updateFund(){
    $('#project_fund_table').bootstrapTable('refresh');
}
function updateFullFund(){
    $('#project_fund_table').bootstrapTable('refresh');
    $('#project_fund_item_table').bootstrapTable('refresh');
    update_project();
}
function updateFundItem(){
    $('#project_fund_item_table').bootstrapTable({
        onLoadSuccess: function(){ updateFundItemBtnHandler();},
        onSearch: function(){ updateFundItemBtnHandler();},
        onSort: function(){  updateFundItemBtnHandler();},
        onToggle: function(){ updateFundItemBtnHandler();},
        onPageChange: function(){ updateFundItemBtnHandler();},
    });
    
    $('#add_fund_item_temp').modalForm({
        modalID: "#create-modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: '/fund/ajax/funditem/add/' + $("#add_fund_item_temp").attr("data-fundPk"),
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
            addModalFormFunction: updateFullFund,
        }
    });
}
function updateFundItemBtnHandler(){
    $(".edit_fundItem").each(function () {
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
                addModalFormFunction: updateFullFund,
            }
        });
    });
    $(".delete_fundItem").each(function () {
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
                addModalFormFunction: updateFullFund,
            }
        });
    });

}
function updateFundBtnHandler(){   

    $(".show_fund").each(function () {

        $(this).click(function(e){
            e.preventDefault();
            fundPk=$(this).data("fund");
            csrftoken = getCookie('csrftoken');
            $.ajax({
                type:"POST",
                url: "/fund/ajax/"+fundPk+"/items/", 
                data:{
                        pk:fundPk,
                        csrfmiddlewaretoken: csrftoken,
                },
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

        })
    });

    $(".edit_fund").each(function () {
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
                addModalFormFunction: updateFund,
            }
        });
    });
    $(".delete_fund").each(function () {
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
                addModalFormFunction: updateFund,
            }
        });
    });

    $(".show_fund").eq(0).trigger("click");
}
function adminActionFund(value, row, index, field){
    action = "<span class='icon-left-cell btn-group'>";
    action += "<button class='icon edit_fund btn btn-success' data-form-url='/fund/ajax/"+row.pk+"/update' ><i type = 'button' class='fas fa-edit'></i></button>";
    action += "<button class='icon show_fund btn btn-secondary' data-fund='"+row.pk+"' ><i type = 'button' class='fas fa-toolbox'></i></button>";
    action += "<button class='icon delete_fund btn btn-danger ' data-form-url='/fund/ajax/"+row.pk+"/delete' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}
function adminActionFundItem(value, row, index, field){
    action = "<span class='icon-left-cell btn-group'>";
    action += "<button class='icon edit_fundItem btn btn-success' data-form-url='/fund/ajax/funditem/"+row.pk+"/update' ><i type = 'button' class='fas fa-edit'></i></button>";
    action += "<button class='icon delete_fundItem btn btn-danger ' data-form-url='/fund/ajax/funditem/"+row.pk+"/delete' ><i type = 'button' class='fas fa-trash'></i></button>";
    action += "</span>"
    return action;
}