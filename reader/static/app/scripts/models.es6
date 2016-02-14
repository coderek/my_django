let Feed = Backbone.Model.extend({
    parse(data) {
        if (_.has(data, 'id') && !this.entries) {
            this.entries = new Entries;
            this.entries.url = `/reader/api/feeds/${data['id']}/entries`;
        }
        return Backbone.Model.prototype.parse.apply(this, arguments);
    }
});
let Feeds = Backbone.Collection.extend({
    model: Feed,
    url: '/reader/api/feeds',
});

let Entry = Backbone.Model.extend({});
let Entries = Backbone.Collection.extend({
    model: Entry,
});

let feeds = new Feeds;
export {feeds};
