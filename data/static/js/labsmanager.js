


// --------------------     Basic Function    ------------------- // 

/**
 * get the cookie information (
 * @param {*} name : the nema of the value to retrieve
 * @returns 
 */
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

/**
 *  Test if an html element is empty
 * @param {*} el : the elemetn to test
 * @returns true if empty or false if filled
 */
function isEmpty( el ){
    return !$.trim(el.html())
}

/**
 * Format a float number to reflect a percentage.
 *
 * @returns {String}
 */

function quotityDisplay(value){
    return parseFloat(value*100).toFixed(0)+" %";
}

function moneyDisplay(value){
    formatter = new Intl.NumberFormat('en-US', {
        // style: 'currency',
        // currency: 'EUR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
      });
    return formatter.format(value).replaceAll(',', ' ')+" EUR";

}

/**
 * test if a selector exist
 * @returns 
 */
jQuery.fn.exists = function(){ return this.length > 0; }
/**
 * Determine whether the given `input` is iterable.
 *
 * @returns {Boolean}
 */
 function isIterable(input) {  
    if (input === null || input === undefined) {
      return false
    }
  
    return typeof input[Symbol.iterator] === 'function'
  }


// --------------------     Basic Table Formatter    ------------------- // 


function quotityFormatter(value, row, index, field){
    return quotityDisplay(value);
}
function quotityAlertFormatter(value, row, index, field){
    if( value == null ){
        return "-";
    }
    val = quotityDisplay(value)
    if(value > 1){
        return "<div class='warning-quotity'>"+val+"</div>";
    }else{
        return "<div class=''>"+val+"</div>";
    }
}


function moneyFormatter(value, row, index, field){
    return moneyDisplay(value);
}

function basicBoolean(value, row, index, field){
    return (value ? '<img src="/static/admin/img/icon-yes.svg" alt="True">' : '<img src="/static/admin/img/icon-no.svg" alt="False">');
}

function styleAlignMiddle(value, row, index, field){
    response={
    //classes: 'text-nowrap another-class',
        css: {"text-align": "center"}
    }
      return response;
}

function employeeFormatter(value, row, index, field){
    if(!isIterable(value)){
        value=[{"employee":value}];
    }
    response = "";
    for (const item of value) {
        //console.log("item :"+JSON.stringify(item));

            tm ="<a href='/staff/employee/"+item.employee.pk+"'>"+item.employee.user_name+"</a>";
            response+= (response.length > 1 ? ', ' : '') + tm;
      }
      return response;
}

function teamMateFormatter(value, row, index, field){
    if(!isIterable(value)){
        value=[{"employee":value}];
    }
    response = "";
    for (const item of value) {
        //console.log("item :"+JSON.stringify(item));
        if (item.employee.is_active == true){

            tm ="<a href='/staff/employee/"+item.employee.pk+"'>"+item.employee.user_name+"</a>";
            response+= (response.length > 1 ? ', ' : '') + tm;
        }
      }
      return response;
}
function ParticipantFormatter(value, row, index, field){
    //console.log('ParticipantFormatter'+JSON.stringify(value))
    //console.log('ParticipantFormatter'+JSON.stringify(row))

    if(!isIterable(value)){
        value=[{"employee":value}];
    }
    response = "";
    for (const item of value) {
        //console.log("item :"+JSON.stringify(item));
        if (item.employee.is_active == true){

            tm ="<a href='/staff/employee/"+item.employee.pk+"'>"+item.employee.user_name;
            if(item.status == "l"){
                tm+= '<sup><i class="fas fa-crown icon-spaced" style="color: coral" title="team leader"></i></sup>';
            }else if(item.status == "cl"){
                tm+= '<sup><i class="fas fa-crown icon-spaced" style="color: cadetblue" title="team leader"></i></sup>';
            }
            tm+="</a>";
            response+= (response.length > 1 ? ', ' : '') + tm;
        }
      }
      return response;
}

function ProjectFormatter(value, row, index, field){
    if(!isIterable(value)){
        value=[{"project":value}];
    }
    response = "";
    for (const item of value) {
        //console.log("item :"+JSON.stringify(item));

            tm ="<a href='/project/"+item.project.pk+"'>"+item.project.name;
            tm+="</a>";
            response+= (response.length > 1 ? ', ' : '') + tm;
      }
      return response;
}


function FundFormatter(value, row, index, field){
    if(!isIterable(value)){
        value=[{"fund":value}];
    }
    response = "<ul>";
    for (const item of value) {
        response +="<li>"+item.funder.short_name;
        response+=" - "+item.institution.short_name;
        response+=" ("+moneyDisplay(item.amount)+")"
        response+="</li>";
      }
      response += "</ul>";
      return response;
}


function projectFormatter(value, row, index, field){
    response = '<a href="/project/'+value.pk+'" >'+value.name+"</a>";
    return response;
}

function dueDatePassed(value, row, index, field){
    curr=new Date();
    valDate=Date.parse(value);
    console.log('date test :'+(curr.getTime()>valDate));
    
    if(curr.getTime()>valDate){
        return '<span class="alert-danger">'+value+'</span>';
    }
    return value
}



// --------------------     Basic Table Sorter    ------------------- // 

function nameSorter(fieldA, fieldB){
    //console.log('[activeSorter] '+JSON.stringify(fieldA)+" / "+JSON.stringify(fieldB)+" / "+JSON.stringify(q));
    A =  fieldA.first_name+" "+fieldA.last_name;
    B = fieldB.first_name+" "+fieldB.last_name;
    if (A <B) return -1;
      if (A > B) return 1;
      return 0;
  }




  // ------------------  ajax load direct --------------  //

  function loadInTemplate(elt, url, data={}, callback=null){
    csrftoken = getCookie('csrftoken');
    defaults={
        csrfmiddlewaretoken: csrftoken
    }
    var datas = $.extend(defaults, data);
    $.ajax({
        type:"GET",
        url: url,
        data:datas,
        success: function( data )
        {
            elt.html(data);
            if(callback)callback();
        },
        error:function( err )
        {
             $("body").html(err.responseText)
            //console.log(JSON.stringify(err));
        }
    })

  }