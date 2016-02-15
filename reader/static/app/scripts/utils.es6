function get_feed_url(ev) {
    return prompt('Feed Address: ');
}

export function try_create_feed(feeds) {
    let url = get_feed_url();
    if (url) {
        feeds.create({url}, {wait: true});
    }
}

export function pad(str, count, s='0') {
    if (!_.isString(str)) {
        str = str.toString();
    }

    if (str.length >= count) {
        return str;
    } else {
        return _.map(_.range(count - str.length), ()=> s).join('') + str;
    }
}
