API_VERSION = 'v0.1'

function submit(){
        var doc_url = $('#doc_url').val();
        var doc_text = $('#doc_text').val();

        var has_url = non_empty(doc_url); 
        var has_text = non_empty(doc_text); 
        var has_text_xor_url = has_text ^ has_url;
        if (! has_text_xor_url) {
                //show modal with input error message
                $('#modal_title').text('Input Error')
                $('#modal_body').html('<p>Please submit a URL <strong>OR</strong> document text.</p>')
                $('#modal_id').modal()
                return
        }
        if (has_text) 
                submit_url(doc_url);
        else 
                submit_text(doc_text);
}


function non_empty(str) {
        return str.trim().length != 0
}


function submit_url(doc_url) {
    $.get({
        url: '/api/'+API_VERSION+'/categorize/url',
        data: {
            'url': doc_url
        },
        cache: false,
        success: submit_success,
        error: submit_error
    })
}

function submit_text(doc_text) {
    $.post({
        url: '/api/'+API_VERSION+'/categorize/text',
        data: doc_text,
        cache: false,
        success: submit_success,
        error: submit_error
    })

}

function submit_success(response) {
    console.log('response')
    console.log(response)
}

function submit_error(xhr) {
    console.log('error')
    console.log(xhr)
}

$('#submit_cat_id').on('click', submit);