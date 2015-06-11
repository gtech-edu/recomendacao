$(document).ready(document_ready());

// Ao carregar a página, realiza os seguintes procedimentos automaticamente:
function document_ready() {
    $('form').submit(false);
    
    $('#btn-enviar-texto').click(function() {
        //var text = $('#form-texto #id_texto').val();
        var text = tinyMCE.activeEditor.getContent({format : 'text'});
        
        $.ajax({
            type: 'POST',
            url: '{% url "envia_texto_sobek" %}',
            data: JSON.stringify({text:text}),
            success: function(response) {
                console.log('Entrada do Sobek: %s', response.text);
                console.log('Saída do Sobek: %s', response.sobek_output);
                
                var element = google.search.cse.element.getElement('gsearch');
                element.execute(response.sobek_output);
            },
            beforeSend: function(jqXHR, settings) {
                jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            }
        });
    });
    
    $('#form-texto').submit(function() {
        //var text = $('#form-texto #id_texto').val();
        var text = tinyMCE.activeEditor.getContent({format : 'text'});
        
        $.ajax({
            type: 'POST',
            url: '{% url "post" %}',
            data: JSON.stringify({text:text}),
            headers: {
                'content-type': 'application/json; charset=utf-8',
                'accept': 'text/html; charset=utf-8'
            },
            success: function(data, status, jqXHR) {
                var newDoc = document.open();
                newDoc.write(jqXHR.responseText);
                newDoc.close();
                
                //var newDoc = window.open();
                //newDoc.document.open();
                //newDoc.document.write(jqXHR.responseText);
                //newDoc.document.close();
            },
            beforeSend: function(jqXHR, settings) {
                jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            }
        });
    });
    
    $('#form-baixar-xml').off('submit');
    $('#form-baixar-xml').submit(function(event) {
        var text = 'xml xml'
        var data = {text:text};
        
        append_hidden_inputs(event.target, data);
        $("#form-baixar-xml").prop('action', '{% url "post" %}.xml');
    });
    
    $('#form-baixar-json').off('submit');
    $('#form-baixar-json').submit(function(event) {
        var text = 'json json';
        var data = {text:text};
        
        append_hidden_inputs(event.target, data);
        $("#form-baixar-json").prop('action', '{% url "post" %}.json');
    });
}

function append_hidden_inputs(form, data) {
    for (i in data) {
        input = $('<input>').prop({'type': 'hidden', 'name': i}).val(data[i]);
        old_input = $(form).find('input[name="' + i +'"]').first();
        input_exists = old_input.length;
        
        if (!input_exists) {
            $(form).append(input);
        }
        else {
            old_input.replaceWith(input);
        }
    }
}

//Scripts do Google Custom Search Engine
function gcseCallback() {
    /*
    if (document.readyState != 'complete') {
        return google.setOnLoadCallback(gcseCallback, true);
    }
    */
    google.search.cse.element.render({gname:'gsearch', div:'results', tag:'searchresults-only', attributes:{linkTarget:''}});
};
window.__gcse = {
    parsetags: 'explicit',
    callback: gcseCallback
};
(function() {
    var cx = '000692798276607258081:hnimutzrgnk';
    var gcse = document.createElement('script');
    gcse.type = 'text/javascript';
    gcse.async = true;
    gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
        '//cse.google.com/cse.js?cx=' + cx;
    var s = document.getElementsByTagName('script')[0];
    s.parentNode.insertBefore(gcse, s);
})();
