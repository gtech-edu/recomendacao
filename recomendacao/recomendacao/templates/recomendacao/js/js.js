$(document).ready(documentReady());

// Ao carregar a página, realiza os seguintes procedimentos automaticamente:
function documentReady() {
    $('form').submit(false);
    
    $('#btn-enviar-texto').click(function() {
        var texto = $('#form-texto #id_texto').val();
        
        $.ajax({
            type: 'POST',
            url: '{% url "envia_texto_sobek" %}',
            data: JSON.stringify({texto:texto}),
            success: function(response) {
                console.log('Entrada do Sobek: %s', response.texto);
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
        var texto = $('#form-texto #id_texto').val();
        
        $.redirect('{% url "resultados" %}', JSON.stringify({texto:texto}));
    });
    
    // Scripts do Google Custom Search Engine
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
}