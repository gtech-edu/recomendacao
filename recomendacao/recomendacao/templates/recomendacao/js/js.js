$(document).ready(document_ready());

// Ao carregar a página, realiza os seguintes procedimentos automaticamente:
function document_ready() {
    $('#form-texto').submit(function(event) {
        //var text = $('#form-texto #id_text').val();
        var text = tinyMCE.activeEditor.getContent({format : 'text'});
        
        $.ajax({
            type: 'POST',
            url: '{% url "envia_texto_sobek" %}',
            data: JSON.stringify({text:text}),
            success: function(response) {
                var sobek_output = '';
                
                for (word in response.sobek_output) {
                    sobek_output += response.sobek_output[word] + ',';
                }
                sobek_output = sobek_output.slice(0, -1);
                
                console.log('Saída do Sobek: %s', sobek_output);
                
                var element = google.search.cse.element.getElement('gsearch');
                element.execute(response.sobek_output);
            },
            beforeSend: function(jqXHR, settings) {
                jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            }
        });
        
        return false;
    });
    
    $('#form-texto-post').submit(function(event) {
        var text = tinyMCE.activeEditor.getContent({format : 'text'});
        var data = {text:text};
        
        append_hidden_inputs(event.target, data);
        $(event.target).prop('action', '{% url "post" %}');
    });
}

function append_hidden_inputs(form, data) {
    for (i in data) {
        input = $('<input>').prop({'type': 'hidden', 'name': i}).val(data[i]);
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
