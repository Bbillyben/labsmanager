(function ($) {
    var elts;
    var settingsCal;
    function calendar_refresh(){
        //console.log("calendar_refresh")
        $('#calendar-box').unbind('click');
        calendar.refetchEvents(); 
        calendar.refetchResources();
        callEventCallback(settingsCal);
    }

    function eventClicked(info){
        $(info.el).tooltip('dispose');
        $('.popover').popover('dispose');
        if (info.event.display == "background" )return  { html: "" }
        // console.log(JSON.stringify(info.event))
        titleP ='<div class="d-flex flex-wrap">'
        titleP += "<b>"+info.event.extendedProps.type+"</b>";
        titleP += '<span class="flex" style="flex-grow: 1;"></span>';
        titleP += '<div class="btn-group" role="group">';
        titleP += '<button type="button" id="popover_close" class="btn btn-close close" ></button>',
        titleP += '</div>';
        titleP += '</div>';
        textP = "<em><b>" + info.event.extendedProps.employee + "</b></em>";
        var d = new Date(info.event.end);
        if(d.getUTCHours()==0)d.setDate(d.getDate() - 1)
        textP += "</br>" + info.event.start.toLocaleDateString() + "<small> (" + info.event.extendedProps.start_period_di+")</small> " + " - " + d.toLocaleDateString() + "<small> (" + info.event.extendedProps.end_period_di+")</small>";
        if(info.event.extendedProps.comment) textP +="</br><i>"+ info.event.extendedProps.comment+"</i>";
        if(USER_PERMS.includes("leave.change_leave") || USER_PERMS.includes("leave.delete_leave") || USER_PERMS.includes("staff.view_employee")){
            textP +="<hr/>";
            textP +="<div class='d-flex flex-wrap btn-group btn-group-sm' role='group'>";
            //textP +="<span class='btn-group'>";
            if(USER_PERMS.includes("leave.change_leave"))textP +="<button class='icon edit_leave btn btn-success' data-form-url='/calendar/update/"+info.event.extendedProps.pk+"/' title='edit leave'><i type = 'button' class='fas fa-edit'></i></button>";
            if(USER_PERMS.includes("staff.view_employee")) textP +="<a role='button' class=' btn btn-secondary' href='/staff/employee/"+info.event.extendedProps.employee_pk+"' title='navigate to user'><i type = 'button' class='fas fa-user'></i></a>"; 
            if(USER_PERMS.includes("is_staff"))textP +="<a role='button' class=' btn btn-primary'  href='/admin/leave/leave/"+info.event.extendedProps.pk+"/change/' title='see in admin'><i type = 'button' class='fas fa-shield-halved'></i></a>"; 
            //textP += '<span class="flex" style="flex-grow: 1;min-width:1.5em;"></span>';
            if(USER_PERMS.includes("leave.delete_leave"))textP +="<button class='icon delete_leave btn btn-danger ' data-form-url='/calendar/delete/"+info.event.extendedProps.pk+"/' title='delete leave'><i type = 'button' class='fas fa-trash'></i></button>";
            //textP +="</span>";

            textP +="</div>";

        }
        

        $(info.el).popover({
            title: titleP,
            content: textP,
            container: 'body',
            trigger: 'click',
            animation: true,
            html:true,
            placement: 'top',
            delay: { "show": 50, "hide": 50 },
            sanitize  : false,
        });
        // $(info.el).on('shown.bs.popover', function () {
        //     this.onclick = function() { alert($(this).text()); };
        //   });

        $(info.el).popover('show');
        updateLeaveButtonHandler();

    }


    function updateLeaveButtonHandler(){
        $("#popover_close").click(function(){$('.popover').popover('dispose');})
        $(".edit_leave").each(function () {
            $(this).labModalForm({
                formURL:  $(this).data("form-url"),
                addModalFormFunction: calendar_refresh,
                modal_title:"Edit Leave",
            })
            $(this).click(function(){$('.popover').popover('dispose');})
        });
        $(".delete_leave").each(function () {
            
            $(this).labModalForm({
                formURL:  $(this).data("form-url"),
                isDeleteForm: true,
                addModalFormFunction: calendar_refresh,
                modal_title:"Delete Leave",
            })
            $(this).click(function(){$('.popover').popover('dispose');})
        });
    }

    function getExtraSetting(){
        var extraSetting={};
        if(typeof settingsCal.extraParams === 'function'){
            extraSetting=settingsCal.extraParams();
        }else{
            extraSetting=settingsCal.extraParams
        }

        // to specify it's from calendar
        extraSetting["cal"]=1;
        return  extraSetting
    }
    function getExtraSettingURL(){
        
        extraSetting=getExtraSetting();
        extraSettingStr=""
        for (s in extraSetting) {
            extraSettingStr+="&"+s+"="+extraSetting[s]
        }

        return extraSettingStr;
    }
    // ---------------------- Selection de date  --------------------- //
    function eventSelectHandler(info){
        // console.log("[eventSelectHandler] :"+JSON.stringify(info))
        $('.popover').popover('dispose');
        $(info.el).tooltip('dispose');

        var d = new Date(info.end);
        d.setDate(d.getDate() - 1)
        modURL=Urls['add_leave']()+"?start_date="+info.start.toISOString()+"&end_date="+d.toISOString();
        modURL+=getExtraSettingURL();
        resource=info.resource
        if(resource){
            modURL+="&employee="+resource.id
        }
        try{
            //$('#detail-panels').unbind('click');
            $(elts).modal('dispose');
        }catch (error) {
            console.log(error);
        }
        
        $(elts).labModalForm({
            formURL: modURL,
            addModalFormFunction: calendar_refresh,
            forceExitFunction: true,
            modal_title:"Leave",
        })
        
    }

    // -------------------------  Update Event Functions --------------- //
    function LeaveChangeHandler(evt){
        $('.popover').popover('dispose');
        $(evt.el).tooltip('dispose');
        datas=evt['event'];
        console.log("LeaveChangeHandler called"+JSON.stringify(datas));
        ne={};
        ne["pk"]=datas["extendedProps"]["pk"];
        ne["employee"]=datas["extendedProps"]["employee_pk"];
        ne["type"]=datas["extendedProps"]["type_pk"];
        ds=datas["start"].toISOString().split('T');
        ne["start_date"]=ds[0];
        if(ds[1].substring(0, 2)== "12"){
            ne["start_period"]="MI"
        }else{
            ne["start_period"]="ST"
        }


        if(datas["end"]){
            de=datas["end"].toISOString().split('T');            
            if(de[1].substring(0, 2)== "12"){
                ne["end_period"]="MI"
                ne["end_date"]=de[0]
            }else{
                d = new Date(de[0]);
                d.setDate(d.getDate() - 1)
                ne["end_date"]=d.toISOString().split('T')[0];
                ne["end_period"]="EN"
            }
        }else{
            ne["end_date"]=ne["start_date"];
        }
        // console.log("new Event : "+JSON.stringify(ne));
        // ajax
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            headers : {
                'Accept' : 'application/json',
                'Content-Type' : 'application/json'
            },
            url : Urls['api:leave-list']()+ne["pk"]+"/",
            type : 'PATCH',
            data : JSON.stringify(ne),
            success : function(response, textStatus, jqXhr) {
                //console.log("Event Successfully Patched!");
            },
            error : function(jqXHR, textStatus, errorThrown) {
                // log the error to the console
                console.log("The following error occured: " + textStatus, errorThrown);
            },
            complete : function() {
                calendar.refetchEvents();
                callEventCallback(settingsCal);
            }
        });
    }

    function callEventCallback(settings){
        if(undefined != settings.eventCallback)settings.eventCallback();
    }
    function getDayHtml(start, end){}
    function eventContentRender(event, createElement){
        // console.log('[eventContentRender] called')
        // console.log(JSON.stringify(event))
        // console.log(event.view.type)
        htmlEvt = ""
        
        if (event.event.display == "background" )return  { html: "" }


        if(event.view.type.toUpperCase().includes("YEAR")){
            start=event.event.start
            end = event.event.end         
            if (end.getUTCHours() != 12 )end.setDate(end.getDate()-1)
            const day1 = start.getDate();
            const month1 = start.getMonth()+1;
            const day2 = end.getDate();
            const month2 = end.getMonth()+1;

            dateField=day1 + (month1 != month2 ? "/" + month1:"") + ( day1 != day2 || month1 != month2 ? ' → ' + day2 + (month1 != month2 ? "/" + month2:""):"")
            htmlEvt = ' <span style="font-size:0.7em;font-weight:italic;">'+ dateField +' ⦿ </span>'+" "+htmlEvt;
        }



        props = event.event.extendedProps
        if(event.view.type.toUpperCase().includes("RESOURCE")){
            htmlEvt += "<span class='resource-name'>"+props.type+"</span>" + '<span class="initial-circle"><span class="initial-circle-inner">'+ getInitials(props.employee).join('')+'</span></span>';
            htmlEvt = "<div class='ressource-cont'>"+htmlEvt+"</div>"
        }else if(event.view.type.toUpperCase().includes("GRID")){
            htmlEvt += props.employee + ' <small>-'+ props.type+'</small>';
        }else{
            htmlEvt += props.employee + " - " + props.type;
        }

        


        if (props.start_period_di == "Middle" ||  props.end_period_di== "Middle"){
            // console.log(event)
            htmlEvt = '<span style="width:50%;">'+htmlEvt+'</span>'
        }
        return  { html: htmlEvt }
    }

    $.fn.lab_calendar = function (options) {
        //console.log("Modal Form Call :"+options.formURL);
            // Default settings
            var language = window.navigator.userLanguage || window.navigator.language;
            //console.log(language.split("-")[0])
            var defaults = {
                selectable:false,
                editable:false,
                extraParams:{},
                eventDrop: LeaveChangeHandler,
                eventResize: LeaveChangeHandler,
                eventClick: eventClicked,
                select: eventSelectHandler,
                local: language,
                height:"auto",
                filterResourcesWithEvents:false,
                initialView: 'resourceTimelineMonth',
                useDatePicker: true,
                headerToolbar: {
                    left: 'prev,next today datePickerButton',
                    center: 'title',
                    right: 'resourceTimelineMonth,resourceBiMensualCustom,resourceYearCustom,resourcefortnightCustom dayGridMonth,dayGridWeek,listWeek,timelineYearCustom resourceMensualWeekSlide'
                },
                cal_type:'default'
            };

            // Extend default settings with provided options
            settingsCal = $.extend(defaults, options);
            elts=this;


            var globals={
                schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',
                
                timeZone: 'UTC',
                locale:settingsCal.local,
                initialView: settingsCal.initialView,
                headerToolbar:settingsCal.headerToolbar,
                eventSources:[{
                        url: Urls['api:leave-search-calendar'](),
                        method: 'GET',
                        extraParams:getExtraSetting,
                    },
                    {
                        url: Urls['vacation_events'](),
                        method: 'GET',
                        extraParams:getExtraSetting,
                    },
                    ],
                resources:{
                        url: Urls['api:employee-calendar-resource'](),
                        method: 'GET',
                        extraParams:getExtraSetting,
                    },
                resourceGroupField:"employee",
                resourceAreaWidth:"10%",
                selectable: settingsCal.selectable,
                editable: settingsCal.editable,
                // eventDidMount: function(info) {
                //     $(info.el).tooltip({
                //     title: info.event.title,
                //     placement: 'top',
                //     trigger: 'hover',
                //     container: 'body',
                //     });
                // },
                eventDrop: settingsCal.eventDrop,
                eventResize: settingsCal.eventResize,
                eventClick: settingsCal.eventClick,
                select: settingsCal.select,
                height: settingsCal.height,
                resourceLabelContent : function(renderInfo) {
                    htmlRes=renderInfo.fieldValue
                    if(USER_PERMS.includes("staff.view_employee")){
                        htmlRes +=" <sup> <a href='"+Urls['employee'](renderInfo.resource._resource.id)+"' title='navigate to employee'><i type = 'button' class='fa-regular fa-circle-right d-print-none text-info'></i></a></sup>"; 
                    } 
                    //htmlRes+="</span>"
                    
                    return { html: htmlRes}
                    },
                    resourceOrder: 'title',
                filterResourcesWithEvents:settingsCal.filterResourcesWithEvents,
                // -------------------------------
                slotDuration: {
                    "hours": 12
                  },
                slotLabelInterval: {
                "hours": 24
                },
                slotLabelFormat: [{
                    month: 'long',
                    week: "short",
                }, // top level of text
                {
                    weekday: 'short',
                    day: 'numeric'
            
                } // lower level of text
                ],

                  // ------------------------------------------
                
                  eventContent:eventContentRender,  
                  eventDisplay:'block',
            }
            // activate plugins
            // globals.plugins=[
            //     adaptivePlugin,
            // ]
            // add date picker button
            if (settingsCal.useDatePicker == true){
                globals.customButtons={
                    datePickerButton: {
                        text:'select',
                        click: function () {      
                            var $btnCustom = $('.fc-datePickerButton-button'); // name of custom  button in the generated code
                            $btnCustom.after('<input type="hidden" id="hiddenDate" class="datepicker"/>');
        
                            $("#hiddenDate").datepicker({
                                showOn: "button",
        
                                dateFormat:"yy-mm-dd",
                                onSelect: function (dateText, inst) {
                                    //$(this).fullCalendar('gotoDate', dateText);
                                    calendar.gotoDate(dateText);
                                },
                                beforeShow: function() {
                                    setTimeout(function(){
                                        $('.ui-datepicker').css('z-index', 99999999999999);
                                    }, 0);
                                },
                            });
        
                            var $btnDatepicker = $(".ui-datepicker-trigger"); // name of the generated datepicker UI 
                            //Below are required for manipulating dynamically created datepicker on custom button click
                            $("#hiddenDate").show().focus().hide();
                            $btnDatepicker.trigger("click"); //dynamically generated button for datepicker when clicked on input textbox
                            $btnDatepicker.hide();
                            $btnDatepicker.remove();
                            $("input.datepicker").not(":first").remove();//dynamically appended every time on custom button click
        
                        }
                    },
                }
            }

            // add pref save
            globals.viewClassNames =function(arg){
                localStorage.setItem(`labsmanager-calendar-view_`+settingsCal.cal_type, arg.view.type);
            }

            // add customs views
            /* TODO : only add necessary views */
            globals.views= {
                timelineYearCustom: {
                    type: 'timeline',
                    buttonText: 'Year',
                    dateIncrement: { years: 1 },
                    slotDuration: { months: 1 },
                    slotLabelInterval: {
                        "month": 1
                        },
                        slotLabelFormat: [{
                            month: 'long',
                            week: "short",
                        }, // top level of text
                        ],
                    visibleRange: function (currentDate) {
                        const start = new Date(currentDate);
                        start.setMonth(0);
                        start.setDate(1);
                        const end = new Date(currentDate);
                        end.setMonth(11);
                        end.setDate(31);
                        return {
                            start: start.toISOString(),
                            end: end.toISOString()
                        };
                    }
                }, 
                resourceYearCustom: {
                    type: 'resourceTimeline',
                    buttonText: 'Year',
                    dateIncrement: { years: 1 },
                    slotDuration: { months: 1 },
                    slotLabelInterval: {
                        "month": 1
                        },
                        slotLabelFormat: [{
                            month: 'long',
                            week: "short",
                        }, // top level of text
                        ],
                    visibleRange: function (currentDate) {
                        const start = new Date(currentDate);
                        start.setMonth(0);
                        start.setDate(1);
                        const end = new Date(currentDate);
                        end.setMonth(11);
                        end.setDate(31);
                        return {
                            start: start.toISOString(),
                            end: end.toISOString()
                        };
                    }
                }, 
                resourcefortnightCustom: {
                    type: 'resourceTimeline',
                    buttonText: 'fortnight',
                    dateIncrement: { weeks: 1 },
                    slotLabelFormat: [{
                        month: 'long',
                    }, // top level of text
                    {
                        weekday: 'short',
                        day: 'numeric',
                
                    }, // lower level of text
                    ],
                    slotDuration: {
                            "hours": 12
                          },
                    slotLabelInterval: {
                        "hours": 24
                        },
                    visibleRange: function (currentDate) {
                        const start = new Date(currentDate);
                        start.setDate(start.getDate() - (start.getDay() + 6) % 7); // previous monday
                        const end = new Date(start);
                        end.setDate(start.getDate()+13);
                        return {
                            start: start.toISOString(),
                            end: end.toISOString()
                        };
                    }
                }, 
                resourceMensualWeekSlide: {
                    type: 'resourceTimeline',
                    buttonText: 'Month',
                    dateIncrement: { weeks: 1 },
                    slotDuration: {
                        "hours": 12
                      },
                    slotLabelInterval: {
                        "hours": 24
                    },
                    slotLabelFormat: [{
                        month: 'long',
                    }, // top level of text
                    {
                        weekday: 'short',
                        day: 'numeric',
                
                    }, // lower level of text
                    ],
                    visibleRange: function (currentDate) {
                        const start = new Date(currentDate);
                        start.setDate(start.getDate() - (start.getDay() + 6) % 7); // previous monday
                        const end = new Date(start);
                        end.setDate(start.getDate()+31);
                        end.setDate(end.getDate() - (end.getDay() + 6) % 7);
                        return {
                            start: start.toISOString(),
                            end: end.toISOString()
                        };
                    }
                }, 
                resourceBiMensualCustom: {
                    type: 'resourceTimeline',
                    buttonText: 'Bi Mensual',
                    dateIncrement: { months: 1 },
                    slotDuration: { days: 1 },
                    slotLabelInterval: {
                        "days": 1
                    },
                    slotLabelFormat: [{
                        month: 'long',
                    }, // top level of text
                    {
                        day:'numeric',
                
                    }, // lower level of text
                    ],
                    visibleRange: function (currentDate) {
                        const start = new Date(currentDate);
                        start.setDate(1);
                        const end = new Date(currentDate);
                        end.setMonth(end.getMonth() + 2); // Ajoute 2 mois à la date de fin
                        end.setDate(-1);
                        return {
                            start: start.toISOString(),
                            end: end.toISOString()
                        };
                    }
                }, 

            }

            eltCal=document.getElementById(this.attr('id'))
            calendar = new FullCalendar.Calendar(eltCal, globals)
            calendar.render();
            return calendar;
        };


}(jQuery));