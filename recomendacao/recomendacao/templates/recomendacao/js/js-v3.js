// Ao carregar a página, realiza os seguintes procedimentos automaticamente:
jQuery(document).ready(function($) {
    //$('#btn-enviar-texto-ajax').click(function(event) {
    $('#form-texto-post').submit(function(event) {
        var text = tinyMCE.activeEditor.getContent({format : 'text'});
        var mode = $('#id_mode').val();
        var images = $('#id_images').prop('checked');
        var data = {text: text, mode: mode, images: images};
        
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '{% url "post-v3" %}',
            data: JSON.stringify(data),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response) {
                $.ajax({
                    type: 'POST',
                    url: '{% url "resultados-v3" %}',
                    data: JSON.stringify(response),
                    contentType: 'application/json',
                    dataType: 'html',
                    success: function(resultados) {
                        $('#results-ajax').html(resultados);
                    },
                    beforeSend: function(jqXHR, settings) {
                        jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
                    }
                });
            },
            beforeSend: function(jqXHR, settings) {
                jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            }
        });
    });
});
