function simpleFormatter(value, row, index, field){
    //console.log('simpleFormatter : '+JSON.stringify(value)+" - row : "+JSON.stringify(row) + "  - index :"+index+ " - fiels :"+field);
    response="";
    switch(field) {
        case 'is_active':
          if(this.allow == 'True'){
            response=(row.user.is_active ? '<i class="fa fa-toggle-off" aria-hidden="true" style="color:green">' : '<i class="fa fa-toggle-on" aria-hidden="true" style="color:red"></i>');
            response = '<span type="button" class="user_action" action-type="activate_user_'+(!row.user.is_active)+'" pk="'+row.user.pk+'">'+response+'</span>'
          }else{
            response=(row.user.is_active ? '<img src="/static/admin/img/icon-yes.svg" alt="True">' : '<img src="/static/admin/img/icon-no.svg" alt="False">');
          }
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
        case 'is_active':
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
    //console.log('userFormatter : '+JSON.stringify(value)+" - row : "+JSON.stringify(row) + "  - index :"+index+ " - fiels :"+field+"  # allow :"+this.allow);
    response =  '<span class="icon-right-cell"><a href="/staff/employee/'+row.pk+'" title="/staff/employee/'+row.ipkd+'/"> '+value.first_name+" "+value.last_name+'</a>';
    response += '<span class="icon-left-cell">';
  if(row.is_team_leader){
    response+='<i class="fas fa-crown icon-spaced" style="color: coral" title="team leader"></i>'
  }
  if(row.is_team_mate){
    response+='<i class="fas fa-user-friends icon-spaced" style="color: cadetblue" title="team mate"></i>'
  }
  response += '</span>';

    return response;
}

function statusFormatter(value, row, index, field){
  response = '';
  //console.log('statusFormatter : '+JSON.stringify(value)+" - row : "+JSON.stringify(row) + "  - index :"+index+ " - fiels :"+field+"  # allow :"+this.allow);
  for (const item of value) {
    if (item.end_date == null){
      response+= (response.length > 1 ? ', ' : '') + item.type.shortname
    }
  }

  return response;
}

function adminActionFormatter(value, row, index, field){
  action = "<span class='icon-left-cell edit_employee' data-form-url='/staff/employee/udpate/"+row.pk+"' ><i type = 'button' class='fas fa-edit'></i></span>";

  return action;
}