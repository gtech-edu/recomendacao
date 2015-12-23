// Checa se "pagina" é igual ao referer (URL sem o domínio) da página atual.
function pagina_atual(pagina) {
    return window.location.pathname == pagina;
}

//Checa se "pagina" é substring da URL da página atual.
function pagina_atual_substring(pagina) {
    return window.location.href.indexOf(pagina) > -1;
}

// Substitui as vírgulas de um string por pontos.
function replaceCommaWithDot(string) {
    if (string) {
        string = string.replace(/,/g,'.');
    }
    return string;
}

// Substitui os pontos de um string por vírgulas.
function replaceDotWithComma(string) {
    if (string) {
        string = string.replace(/./g,',');
    }
    return string;
}

function round_number(num, dec) {
    return Math.round(num * Math.pow(10, dec)) / Math.pow(10, dec);
}

function resetForm($form) {
// to call, use:
// resetForm($('#myform')); // by id, recommended
// resetForm($('form[name=myName]')); // by name
    $form.find('input:text, input:password, input:file, input[type="email"], select, textarea').val('');
    $form.find('input:radio, input:checkbox')
         .removeAttr('checked').removeAttr('selected');
}

//Limpa as mensagens de erro.
function limpa_error_msg() {
    $('.error_msg').html('');
}

function limpa_select(select_selector) {
    $(select_selector).select2('val', '');
}

function getUrlVars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

function formReturnKey(event, input_text_types) {
    var text_fields = $(event.delegateTarget).find(input_text_types);
    var event_field_index = $(text_fields).index(event.target);
    var next_field_index = event_field_index + 1;
    
    if (event.keyCode == 13) {
        event.preventDefault();
        
        while ($(text_fields[next_field_index]).prop('disabled')) {
            next_field_index += 1;
        }
        
        if (next_field_index < text_fields.length) {
            $(text_fields[next_field_index]).focus();
        }
        else {
            $(event.target).submit();
            //$(text_fields[0]).focus();
            $(event.target).blur();
        }
    }
}

function append_hidden_inputs(form, data) {
    for (i in data) {
        input = $('<input/>').prop({'type': 'hidden', 'name': i}).val(data[i]);
        old_input = $(form).find('[name="' + i +'"]').first();
        input_exists = old_input.length;
        
        if (!input_exists) {
            $(form).append(input);
        }
        else {
            old_input.replaceWith(input);
        }
    }
}

function convert_list_of_strings_to_string(list) {
    var output_string = '';
    for (string_index in list) {
        output_string += list[string_index] + ',';
    }
    output_string = output_string.slice(0, -1);
    return output_string;
}

function is_defined(variable) {
    if (typeof variable !== 'undefined') {
        return true; // variable is defined
    }
    else {
        return false; // variable is undefined
    }
}

function is_substring_of_string(substring, string) {
    return string.indexOf(substring) > -1;
}

function is_element_of_array(element, array) {
    return array.indexOf(element) > -1;
}
