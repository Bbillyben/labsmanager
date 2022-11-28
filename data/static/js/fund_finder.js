var user_id = 0;
var project_id = 0;

function initFundFinder(user_idA){
    user_id=user_idA;
    var filters = loadTableFilters('project');

    var options={
        queryParams: filters,
        name:'funditem',
        
    }
    setupFilterList('funditem', $('#fund_main_table'));
    $('#fund_main_table').labTable(options);

}