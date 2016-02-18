let Feed = Backbone.Model.extend({
    parse(data) {
        if (_.has(data, 'id') && !this.entries) {
            this.entries = new Entries;
            this.entries.url = `/reader/api/feeds/${data['id']}/entries`;
        }
        return Backbone.Model.prototype.parse.apply(this, arguments);
    },
    refresh() {
        this.fetch({data: {refresh: true}}).then(()=>this.entries.fetch());
    }
});
let Feeds = Backbone.Collection.extend({
    model: Feed,
    url: '/reader/api/feeds',
});

let Entry = Backbone.Model.extend({
    defaults: {
        'title': '',
        'summary': '',
        'content': '',
        'published': '',
        'url': '',
    },
    isNewEntry() {
        let published_date = this.get('published');
        let today = new Date();
        return today.getYear() == published_date.getYear() &&
            today.getMonth() == published_date.getMonth() &&
            today.getDate() == published_date.getDate();
    },
    parse(data) {
        if (data['published']) {
            data['published'] = new Date(data['published']);
        }
        return data;
    },
    content() {
        return this.get('content') || this.get('summary');
    }
});
let Entries = Backbone.Collection.extend({
    comparator(e1, e2) {
        let p1 = e1.get('published').valueOf();
        let p2 = e2.get('published').valueOf();
        return p1 < p2 ? 1 : -1;
    },
    model: Entry,
});

let feeds = new Feeds;
export {feeds};
