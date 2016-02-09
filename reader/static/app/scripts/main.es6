import './setup';
import * as utils from './body';
import models from './api';

let feeds = new models.Feeds;

$(function () {
    $('#add_feed').click(function () {
        var url = utils.get_feed_url();
        if (url) {
            feeds.create({url: url});
        }
    });
});
