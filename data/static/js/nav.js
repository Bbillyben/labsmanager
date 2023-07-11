//  Credit : Inventree https://github.com/inventree/InvenTree
/*
 * Activate (display) the selected panel
 */
function activatePanel(label, panel_name, options={}) {

    // First, cause any other panels to "fade out"
    $('.panel-visible').hide();
    $('.panel-visible').removeClass('panel-visible');

    // Find the target panel
    var panel = `#panel-${panel_name}`;
    var select = `#select-${panel_name}`;

    // Check that the selected panel (and select) exist
    if ($(panel).length && $(select).length) {
        // Yep, both are displayed
    } else {
        // Either the select or the panel are not displayed!
        // Iterate through the available 'select' elements until one matches
        panel_name = null;

        $('.sidebar-selector').each(function() {
            var name = $(this).attr('id').replace('select-', '');

            if ($(`#panel-${name}`).length && (panel_name == null)) {
                panel_name = name;
            }

            panel = `#panel-${panel_name}`;
            select = `#select-${panel_name}`;
        });
    }
    // Save the selected panel
    localStorage.setItem(`labsmanager-selected-panel-${label}`, panel_name);

    // Display the panel
    $(panel).addClass('panel-visible');

    // Load the data
    $(panel).trigger('fadeInStarted');

    $(panel).fadeIn(300, function() {
    });

    // Un-select all selectors
    $('.list-group-item').removeClass('active');

    // Find the associated selector
    var selector = `#select-${panel_name}`;

    $(selector).addClass('active');

    // check if parent is accordion if show ensure it's open
    var selparent = $(selector).parent()
    if(undefined != selparent.data("bs-parent")){
        selparent.collapse('show')
    }
    
}


function onPanelLoad(panel, callback) {
    // One-time callback when a panel is first displayed
    // Used to implement lazy-loading, rather than firing
    // multiple AJAX queries when the page is first loaded.

    var panelId = `#panel-${panel}`;

    $(panelId).on('fadeInStarted', function() {

        // Trigger the callback
        callback();

        // Turn off the event
        $(panelId).off('fadeInStarted');

    });
}

/**
 * Enable support for sidebar on this page
 */
 function enableSidebar(label, options={}) {

    // Enable callbacks for sidebar buttons
    $('.sidebar-selector').click(function() {
        var el = $(this);

        // Find the matching panel element to display
        var panel_name = el.attr('id').replace('select-', '');

        activatePanel(label, panel_name, options);
    });

    // Find the "first" available panel (according to the sidebar)
    var selected_panel = $.urlParam('display') || localStorage.getItem(`labsmanager-selected-panel-${label}`) || options.default;

    if (selected_panel) {
        activatePanel(label, selected_panel);
    } else {
        // Find the "first" available panel (according to the sidebar)
        var selector = $('.sidebar-selector').first();

        if (selector.exists()) {
            var panel_name = selector.attr('id').replace('select-', '');
            activatePanel(label, panel_name);
        }
    }

    if (options.hide_toggle) {
        // Hide the toggle button if specified
        $('#sidebar-toggle').remove();
    } else {
        $('#sidebar-toggle').click(function() {
            // We wish to "toggle" the state!
            var state = localStorage.getItem(`labsmanager-menu-state-${label}`) || 'expanded';

            setSidebarState(label, state == 'expanded' ? 'collapsed' : 'expanded');
        });
    }

   
    // Set the initial state (default = expanded)
    var state = localStorage.getItem(`labsmanager-menu-state-${label}`) || 'expanded';

    setSidebarState(label, state);

    // Finally, show the sidebar
    $('#sidebar').show();

}

/*
 * Set the "toggle" state of the sidebar
 */
function setSidebarState(label, state) {

    if (state == 'collapsed') {
        $('.sidebar-item-text').animate({
            'opacity': 0.0,
            'font-size': '0%',
        }, 100, function() {
            $('.sidebar-item-text').hide();
            $('#sidebar-toggle-icon').removeClass('fa-chevron-left').addClass('fa-chevron-right');
        });
    } else {
        $('.sidebar-item-text').show();
        $('#sidebar-toggle-icon').removeClass('fa-chevron-right').addClass('fa-chevron-left');
        $('.sidebar-item-text').animate({
            'opacity': 1.0,
            'font-size': '100%',
        }, 100);
    }
    //$('#sidebar-toggle').attr('state', state);
    localStorage.setItem(`labsmanager-menu-state-${label}`, state);

}