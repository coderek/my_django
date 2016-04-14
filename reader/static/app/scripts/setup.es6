import * as utils from './utils';
import {default as feeds_tpl} from 'templates/feeds_manager';
import {default as no_feeds_tpl} from 'templates/no_feeds';
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ajaxStart(function () {
    startLoadingAnimation();
});
$(document).ajaxStop(function () {
    stopLoadingAnimation();
});
$(document).ajaxError(function (ev, jqxhr, settings, thrownError) {
    let {status, responseText} = jqxhr;
    toastr.error(status + ': ' + responseText, 'Error');
});

Handlebars.registerHelper('date', function(date, format) {
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    let day = date.getDate();
    return `${year}-${utils.pad(month, 2)}-${utils.pad(day, 2)}`;
});

Handlebars.registerPartial('feeds_tpl', feeds_tpl);
Handlebars.registerPartial('no_feeds_tpl', no_feeds_tpl);


var animationHanlder = null;
var _counter = -1;
function counter() {
    _counter++;
    return _counter;
}
function startLoadingAnimation() {
    $('.loading').fadeIn();
    animationHanlder = setInterval(()=> {
        let c = counter() % 4;
        $('.loading span').hide();
        $('.loading span').each(function () {
            if (c > 0) {
                $(this).show();
            }
            c --;
        });
    }, 100);
}

function stopLoadingAnimation() {
    if (animationHanlder) {
        clearInterval(animationHanlder);
    }
    $('.loading').fadeOut();
}

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

// override mixinTemplateHelpers from marionette
var mixinTemplateHelpers = Marionette.View.prototype.mixinTemplateHelpers;
Marionette.View.prototype.mixinTemplateHelpers = function (data) {
    var data = mixinTemplateHelpers.call(this, data);
    return _.extend(global_context || {}, data);
};
