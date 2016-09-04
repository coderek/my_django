$(function () {
    setupComments();
    loadComments();
});


function setupComments() {
    var name = $('#name');
    var email = $('#email');
    // var test = $('#test');
    var comment = $('#comment');
    var form = $('#comment_form');
    var submitBtn = $('[type=submit]', form);

    form.submit(function () {
        if (!checkValues(name, email, comment)) {
            submitForm(name, email, comment);
        }
        return false;
    });
}


function submitForm(name, email, comment) {
    $.ajax({
        method: 'post',
        url: 'api/comments',
        data: {
            name: name.val(),
            email: email.val(),
            // test: test.val(),
            content: comment.val(),
            post: $('[name=post_id]').val()
        }
    }).then(function (data) {
        loadComments();
        $('[type=email], [type=text], textarea', 'form').val('');
        $('[type=submit]').attr('disabled', false);
        alert('Comment is posted!');
    });
    $('[type=submit]').attr('disabled', true);
}

function loadComments() {
    var postId = $('[name=post_id]').val();
    $.get('api/comments?post=' + postId).then(function (data) {
        renderComments(data);
    });
}

function renderComments(data) {
    var dom = React.DOM;
    var commentEls = _.map(data, function (comment) {
        return dom.li({className: 'comment'},
            dom.p({dangerouslySetInnerHTML: {__html: escapeHtml(comment.content).replace(/\n/g, '<br>')}}),
            dom.div(null,
                dom.span(null, 'Posted by: ' + comment.name),
                dom.time(null, comment.created_at)
            )
        );
    });
    var root = dom.ul.apply(null, [{className: 'comments-container'}].concat(commentEls));
    ReactDOM.render(root, $('#comments').get(0));
}

function checkValues(name, email, comment) {
    var hasError = false;

    _.each([name, email, comment], function (field) {
        field.closest('.input-group').removeClass('has-error');
    });

    _.each([name, email, comment], function (field) {
        if (_.isEmpty(field.val())) {
            hasError = true;
            field.closest('.input-group').addClass('has-error');
        }
    });

    return hasError;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
};

function escapeHtml(string) {
    return String(string).replace(/[&<>"'\/]/g, function (s) {
        return entityMap[s];
    });
}
