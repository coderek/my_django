$(function () {
    $('#add_feed').click(get_feed_url);
});

function get_feed_url(ev) {
    let url = prompt('input url');
    if (url != '') {
        add_feed(url);
    }
}

function add_feed(url) {
}
