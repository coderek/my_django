let Feed = Backbone.Model.extend({});
let Feeds = Backbone.Collection.extend({
    model: Feed,
    url: '/reader/api/feeds',
});

let Entry = Backbone.Model.extend({});
let Entries = Backbone.Collection.extend({
    model: Entry,
});

let feeds = new Feeds;
feeds.on('add', (feed)=> {
    feed.entries = new Entries;
    feed.entries.url = `/reader/api/feeds/${feed.id}/entries`;
});

export {feeds};
