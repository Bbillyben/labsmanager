function simpleFormatter(value, row, index, field){
    response="";
    switch(field) {
        case 'active':
            response=(value ? '<img src="/static/admin/img/icon-yes.svg" alt="True">' : '<img src="/static/admin/img/icon-no.svg" alt="False">');
          break;
        case 'team_leader':
            response=(value ? '<i class="fas fa-crown" style="color: coral" title="leader"></i>' : '');
          break;
        case 'team_participant':
            response=(value ? '<i class="fas fa-user-friends" style="color: cadetblue" title="team mate"></i>' : '');
            break;
        default:
          // code block
      } 

      return response;    
}


function simpleStyle(value, row, index, field){
    response="";
    switch(field) {
        case 'active':
        case 'team_leader': 
        case 'team_participant':
            response={
                //classes: 'text-nowrap another-class',
                css: {"text-align": "center"}
                }
          break;
        default:
          // code block
      } 

      return response;    
}

function userFormatter(value, row, index, field){
    //console.log('userFormatter : '+value+" - row : "+JSON.stringify(row) + "  - index :"+index+ " - fiels :"+field);
    return '<a href="/staff/employee/'+row.id+'" title="/staff/employee/'+row.id+'/"> '+value+'</a>'
}