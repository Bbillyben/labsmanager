
/**
 * Mimicking the Jquery Extends .
 *
 * @returns 
 */

function extend(){
  for(var i=1; i<arguments.length; i++)
      for(var key in arguments[i])
          if(arguments[i].hasOwnProperty(key))
              arguments[0][key] = arguments[i][key];
  return arguments[0];
}


/*
 * Sanitize a string provided by the user from an input field,
 * e.g. data form or search box
 *
 * - Remove leading / trailing whitespace
 * - Remove hidden control characters
 *  Credit : Inventree https://github.com/inventree/InvenTree
 */
function sanitizeInputString(s, options={}) {

    if (!s) {
        return s;
    }

    // Remove ASCII control characters
    s = s.replace(/[\x01-\x1F]+/g, '');

    // Remove Unicode control characters
    s = s.replace(/[\p{C}]+/gu, '');

    s = s.trim();

    return s;
}

/**
 * Format a float number to reflect a percentage.
 *
 * @returns {String}
 */

 function quotityDisplay(value){
    return parseFloat(value*100).toFixed(0)+" %";
}

/**
 * Format a float number to reflect currency in euros (not use € as it crash bottstraptable export).
 *
 * @returns {String}
 */
function moneyDisplay(value){
    formatter = new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
      });
    return formatter.format(value); //.replaceAll(',', ' ')+" EUR";

}

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


  
/**
 * Returns true if the input looks like a valid number
 * @param {String} n
 * @returns
 */
function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

/**
 * Returns true if the input looks like a json
 * @param {String} n
 * @returns
 */
function isJson(item) {
  let value = typeof item !== "string" ? JSON.stringify(item) : item;
  try {
    value = JSON.parse(value);
  } catch (e) {
    return false;
  }

  return typeof value === "object" && value !== null;
}

/**
 * Returns true if the input looks like a email
 * @param {String} n
 * @returns
 */
function isEmail(item) {
  var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  return item.match(validRegex);
}

/**
 * To replicate windows open with POST params.
 * Create a Form and submit it 
 * @returns nothing
 */
function openWindowWithPost(url, data, csrftoken) {
  var form = document.createElement("form");
  form.target = "_blank";
  form.method = "POST";
  form.action = url;
  form.style.display = "none";
  form.header

  for (var key in data) {
      var input = document.createElement("input");
      input.type = "hidden";
      input.name = key;
      input.value = data[key];
      form.appendChild(input);
  }
  const hiddenField = document.createElement('input');
  hiddenField.type = 'hidden';
  hiddenField.name = 'csrfmiddlewaretoken';
  hiddenField.value = csrftoken;
  form.appendChild(hiddenField);

  document.body.appendChild(form);



  form.submit();
  document.body.removeChild(form);
}

/**
 * Validate if a string is a valid email 
 * @returns true/false
 */
function validateEmail(email){
  return email.match(
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  );
};

/**
 * Validate if a string is a valid phone number 
 * @returns true/false
 */
function validatePhone(phone){
  return phone.match(
    /^[\+]?[(]?(?:[0-9]{2,3}[)]?[-\s\.\-])?[0-9]{1,3}(?:[-\s\.\-]?[0-9]{2,6})+$/im
    );
};

/**
 * Format a url type string to add protocole 
 * @returns true/false
 */
function formatAsHTMLLink(inputURL, defaultProtocol="https"){
  url = inputURL.startsWith("http://") || inputURL.startsWith("https://") ? inputURL : defaultProtocol+'://'+ inputURL;
  return url
}
/**
 * Format date string to Iso Format with hour if in 
 * @returns string
 */
function format_date_iso(dateStr, option={}){
  var d = new Date(dateStr);
  const defaults = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  };
  var options = extend(defaults, option);
  var timeString = new Intl.DateTimeFormat('default', options).format(d);

  return timeString
}
/**
 * Create an id from a string, stripping accent and replacing all caracter except letter and number
 * extra_suffix : add an extra chain to be added at the end of the string
 * add_uuid : to add a sort of 36 car UUID at the end of the string
 * @returns string
 */
function createIdFrom(name, extra_suffix = "", add_uuid=false ) {
  let normalized = name.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  let id = normalized.replace(/[^a-zA-Z0-9]+/g, "_");
  id+="_"+extra_suffix;
  if (add_uuid){
    id +=URL.createObjectURL(new Blob()).substr(-36);
  }
    
  return id;
}