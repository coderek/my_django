import {feeds} from './models';
import {get_feed_url} from './body';

let HeaderView = Backbone.View.extend({
    el: '#reader .top',
    events: {
        'click #add_feed': 'create_feed',
    },
    create_feed: function () {
        var url = get_feed_url();
        if (url) {
            feeds.create({url}, {wait: true, success:(m)=>console.log(m)});
        }
    }
});

let headView = new HeaderView;

let FeedsManagerView = Backbone.View.extend({
    el: '#feeds_manager',
    load_feeds: function () {
        this.$('.feeds').empty();
        feeds.each(feed=> {
            var {id, title, description} = feed.toJSON();
            let t = `<li data-id='${id}'>
                <div>${title}</div>
                <div>${description || ''}</div>
            </li>`;
            this.$('.feeds').append(t);
        });

    },
    events: {
        'click .feeds li': 'load_feed_entries'
    },
    load_feed_entries: function (ev) {
        let target = $(ev.currentTarget);
        let feed = feeds.get(target.data('id'));
        entriesManagerView.set_collection(feed.entries);
        feed.entries.fetch();
    },
});


let EntriesManagerView = Backbone.View.extend({
    el: '#entries_manager',
    set_collection: function (collection) {
        if (this.collection)
            this.stopListening(this.collection);

        this.collection = collection;
        this.listenTo(collection, 'sync', this.render);
    },
    render: function () {
        this.$('.entries').empty();
        this.collection.each(entry=> {
            let {id, title, summary} = entry.toJSON();
            let e = `<div data-id='${id}'>
                <div>${title}</div>
                <div>${summary}</div></div>`;

            this.$('.entries').append(e);
        });
    }
});

let feedsManagerView = new FeedsManagerView;
let entriesManagerView = new EntriesManagerView;
feedsManagerView.listenTo(feeds, 'sync', feedsManagerView.load_feeds);
