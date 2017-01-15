API_VERSION = 'v0.1'


jQuery.fn.visible = function() {
    return this.css('visibility', 'visible');
};

jQuery.fn.invisible = function() {
    return this.css('visibility', 'hidden');
};

jQuery.fn.visibilityToggle = function() {
    return this.css('visibility', function(i, visibility) {
        return (visibility == 'visible') ? 'hidden' : 'visible';
    });
};

function scroll_to(element) {
    $('html, body').animate({
        scrollTop: $(element).offset().top
    }, 2000);
}

function non_empty(str) {
        return str.trim().length != 0
}

function submit_doc(){
        clear_feedback();
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
                submit_text(doc_text);
        else 
                submit_url(doc_url);
}

function submit_url(doc_url) {
    console.log('submitting url ' + doc_url);
    $('.spinner').visible()
    $.get({
        url: '/api/'+API_VERSION+'/url',
        data: {
            'url': doc_url
        },
        cache: false,
        success: submit_success_url,
        error: submit_error
    })
}

function submit_text(doc_text) {
    console.log('submitting text ' + doc_text);
    $('.spinner').visible()
    $.post({
        url: '/api/'+API_VERSION+'/text',
        data: doc_text,
        cache: false,
        success: submit_success_text,
        error: submit_error
    })

}



function submit_success_doc(response, show_feedback) {
    var cat = response['category']
    var is_ad = cat == 1;
    console.log(response)
    var msg = '<p>This <strong>IS</strong> an advertorial.</p>';
    if (! is_ad)     
        msg = msg.replace('IS', 'IS NOT');
    $('#show_classification_body_id').html(msg)
    $('.spinner').invisible()
    $('#show_classification_id').show()
    if (show_feedback)
        $('#feedback_request_id').show()

    scroll_to("#show_classification_id")
}

function submit_success_url(response) {
    return submit_success_doc(response, true);
}

function submit_success_text(response) {
    return submit_success_doc(response, false);
}


function submit_error(xhr, status, error) {
    $('.spinner').invisible()
    $('#modal_title').text('Error')
    $('#modal_body').text(xhr.responseText)
    $('#modal_id').modal()
}

function submit_feedback(feedback) {
    $('.spinner').visible()
    $.get({
        url: '/api/'+API_VERSION+'/feedback',
        data: {'feedback': feedback},
        success: submit_success_feedback,
        error: submit_error
    })
}
function submit_success_feedback(response) {
    $('.spinner').invisible()
    $('#feedback_header_id').text('Thanks for the feedback')
    $('#feedback_body_id').text("Now we'll do better next time!")

    $('#feedback_response_id').show()
    scroll_to("#feedback_response_id")
}

function clear_feedback() {
    $('#feedback_request_id').hide()
    $('#show_classification_id').hide()
    $('#feedback_response_id').hide()
}
clear_feedback()
$('#submit_cat_id').on('click', submit_doc);
$('#text_submit_id').on('click', submit_doc);
$('#url_submit_id').on('click', submit_doc);
$('#submit_feedback_true_id').on('click', function() {submit_feedback(true)})
$('#submit_feedback_true_false').on('click', function() {submit_feedback(false)})