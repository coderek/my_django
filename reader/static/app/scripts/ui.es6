import {feeds} from './models';
import {get_feed_url} from './body';
import {default as feed_tpl} from 'templates/feed';
import {default as entry_tpl} from 'templates/entry';
import {default as add_feed_tpl} from 'templates/add_feed';
import {default as feeds_manager_tpl} from 'templates/feeds_manager';
import {default as entries_manager_tpl} from 'templates/entries_manager';
import {default as middle_layout_tpl} from 'templates/middle_layout';

let FeedView = Marionette.ItemView.extend({
    template: feed_tpl,
    tagName: 'li',
    className: 'feed',
    attributes() {
        return {
            'data-id': ()=>this.model.id,
        };
    },
    ui: {
        'title': '.title',
    },
    events: {
        'click @ui.title': 'selected',
    },
    selected() {
        this.model.entries.fetch();
        this.triggerMethod('selected');
    }
});

let FeedsManagerView = Marionette.CompositeView.extend({
    template: feeds_manager_tpl,
    childViewContainer: '.feeds',
    childView: FeedView,
    className: 'feeds-manager',
});

let EntryView = Marionette.ItemView.extend({
    template: entry_tpl,
    className: 'entry',
});


let EntriesManagerView = Marionette.CompositeView.extend({
    template: entries_manager_tpl,
    childViewContainer: '.entries',
    childView: EntryView,
    className: 'entries-manager',
});

export let MiddleLayout = Marionette.LayoutView.extend({
    tagName: 'div',
    className: 'middle-layout row',
    template: middle_layout_tpl,
    regions: {
        'left': '.left.region',
        'right': '.right.region',
    },
    childEvents: {
        'selected': 'showEntries',
    },
    showEntries(childView) {
        console.log(childView);
        this.getRegion('right').show(new EntriesManagerView({
            collection: childView.model.entries,
        }));
    },
    onRender() {
        this.getRegion('left').show(new FeedsManagerView({
            collection: feeds,
        }));
    },
});

export let AddFeedView = Marionette.ItemView.extend({
    template: add_feed_tpl,
    ui: {
        'add_button': '#add_feed',
    },
    events: {
        'click @ui.add_button': 'create_feed',
    },
    create_feed() {
        let url = get_feed_url();
        if (url) {
            feeds.create({url}, {wait: true});
        }
    }
});

