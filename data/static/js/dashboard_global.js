

function loadDashboardCards(){
    console.log("start loadDashboardCards");
    $('.panel-content .card').each(function(){
        url=$(this).data('url');
        if(url==undefined)return;

        console.log('start load : '+url);
        loadInTemplate(elt=$(this),url=url);
    });
}