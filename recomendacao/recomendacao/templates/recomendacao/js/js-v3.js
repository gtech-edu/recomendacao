// Ao carregar a página, realiza os seguintes procedimentos automaticamente:
$(document).ready(function() {
    $('#form-texto-post').submit(function(event) {
        var text = tinyMCE.activeEditor.getContent({format : 'text'});
        var data = {text:text};
        
        append_hidden_inputs(event.target, data);
        $(event.target).prop('action', '{% url "post-v3" %}');
    });
    
    $('#btn-enviar-texto-ajax').click(function(event) {
        var text = tinyMCE.activeEditor.getContent({format : 'text'});
        var mode = $('#id_mode').val();
        
        $.ajax({
            type: 'POST',
            url: '{% url "post-v3" %}',
            data: JSON.stringify({text: text, mode: mode}),
            contentType: 'application/json',
            dataType: 'json',
            success: function(response) {
                var sobek_output = convert_list_of_strings_to_string(response.sobek_output);
                console.log('Saída do Sobek: %s', sobek_output);
                
                var results_container = $('#results-ajax');
                var words_string = '';
                var result = {};
                var results_string = '';
                
                results_container.html('');
                
                if (is_defined(response.sobek_output)) {
                    for (word_index in response.sobek_output) {
                        words_string += response.sobek_output[word_index] + ' ';
                    }
                    words_string = words_string.slice(0, -1);
                    
                    $('<div/>').html(words_string).appendTo(results_container);
                }
                
                if (is_defined(response.results_list)) {
                    for (result_index in response.results_list) {
                        result = response.results_list[result_index];
                        
                        results_string += '' + 
                        '<div>' + 
                            '<div><a href="' + result.url + '" target="_blank">' + result.title_markup + '</a></div>' + 
                            '<div><cite>' + result.url_markup + '</cite></div>' + 
                            '<div>' + result.snippet_markup + '</div>' + 
                        '</div>';
                    }
                    
                    $('<div/>').html(results_string).appendTo(results_container);
                }
            },
            beforeSend: function(jqXHR, settings) {
                jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
            }
        });
    });
});
