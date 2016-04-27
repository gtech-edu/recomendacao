// Ao carregar a página, realiza os seguintes procedimentos automaticamente:
jQuery(document).ready(function($) {
    //$('#btn-enviar-texto-ajax').click(function(event) {
    $('#form-texto-post').submit(function(event) {
        var text = tinyMCE.activeEditor.getContent({format : 'text'});
        var mode = $('#id_mode').val();
        var images = $('#id_images').prop('checked');
        var cache_reload = $('#id_cache_reload').val();
        var data = {text: text, mode: mode, images: images, cache_reload: cache_reload};

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
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(jqXHR.responseJSON);
            },
            beforeSend: function(jqXHR, settings) {
                jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            }
        });
    });
});
