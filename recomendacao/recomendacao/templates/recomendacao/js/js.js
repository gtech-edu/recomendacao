$(document).ready(documentReady());

// Ao carregar a página, realiza os seguintes procedimentos automaticamente:
function documentReady() {
    $('form').submit(false);
    
    $('#form-texto').submit(function() {
        var texto = $('#form-texto #id_texto').val();
        
        $.ajax({
            type: 'POST',
            url: '{% url "envia_texto_sobek" %}',
            data: JSON.stringify({texto:texto}),
            success: function(response) {
                var element = google.search.cse.element.getElement('gsearch');
                element.execute(response.sobek_output);
            },
            beforeSend: function(jqXHR, settings) {
                jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            }
        });
    });
}