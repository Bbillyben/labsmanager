user_id= 0;
function initContractBaseView(user_idA){
    user_id = user_idA;

    
    $('#contract_create').modalForm({
        modalID: "#create-modal",
        modalContent: ".modal-content",
        modalForm: ".modal-content form",
        formURL: '/expense/ajax/contract/add/',
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

}