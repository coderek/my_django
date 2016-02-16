import {feeds} from './models';
import * as utils from './utils';
import {default as feed_tpl} from 'templates/feed';
import {default as entry_tpl} from 'templates/entry';
import {default as top_region_tpl} from 'templates/top_region';
import {default as feeds_manager_tpl} from 'templates/feeds_manager';
import {default as entries_manager_tpl} from 'templates/entries_manager';
import {default as middle_layout_tpl} from 'templates/middle_layout';
import {default as no_feeds_tpl} from 'templates/no_feeds';

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
        'click': 'selected',
    },
    selected() {
        this.model.entries.fetch();
        this.$el.addClass('selected');
        this.triggerMethod('feed:selected');
    }
});

let EmptyFeedsView = Marionette.ItemView.extend({
    template: no_feeds_tpl,
    className: 'empty-view',
    events: {
        'click .js-add-feed': 'create_feed',
    },
    create_feed() {
        utils.try_create_feed(feeds);
    }
});

let FeedsManagerView = Marionette.CompositeView.extend({
    template: feeds_manager_tpl,
    childViewContainer: '.feeds',
    childView: FeedView,
    className: 'feeds-manager',
    emptyView: EmptyFeedsView,
    onRenderCollection () {
        this.children.first().selected();
    },
    childEvents: {
        'feed:selected' (view) {
            this.children.each( v => {
                if (v != view && v.$el.is('.selected')) {
                    v.$el.removeClass('selected');
                }
            });
        }
    }
});

let EntryView = Marionette.ItemView.extend({
    template: entry_tpl,
    className: 'entry',
    ui: {
        'entry_content': '.content',
    },
    events: {
        'click .title': 'openEntry',
    },
    openEntry() {
        if (this.$el.is('.open')) {
            this.$el.removeClass('open');
            return;
        }

        this.ui.entry_content.html(this.model.content());
        this.$el.addClass('open');
    }
});


let EntriesManagerView = Marionette.CompositeView.extend({
    template: entries_manager_tpl,
    childViewContainer: '.entries',
    childView: EntryView,
    className: 'entries-manager',
    ui: {
        'refresh_btn': '.js-refresh-feed',
    },
    events: {
        'click @ui.refresh_btn': 'refreshFeed',
    },
    refreshFeed() {
        this.triggerMethod('feed:refresh')
    }
});

export let MiddleLayout = Marionette.LayoutView.extend({
    tagName: 'div',
    className: 'middle-layout',
    template: middle_layout_tpl,
    regions: {
        'left': '.left.region',
        'right': '.right.region',
    },
    childEvents: {
        'feed:selected': 'showEntries',
        'feed:refresh': 'refreshSelectedFeed',
    },
    showEntries(childView) {
        let selected_feed = childView.model;
        this.getRegion('right').show(new EntriesManagerView({
            collection: selected_feed.entries,
        }));
        this.selected_feed = selected_feed;
    },
    refreshSelectedFeed(childView) {
        let selected_feed = this.selected_feed;
        if (selected_feed) {
            selected_feed.refresh();
        }
    },
    onRender() {
        this.getRegion('left').show(new FeedsManagerView({
            collection: feeds,
        }));
    },
});

export let TopRegionView = Marionette.ItemView.extend({
    template: top_region_tpl,
    className: 'container',
    ui: {
        'add_button': '#add_feed',
    },
    events: {
        'click @ui.add_button': 'create_feed',
    },
    create_feed() {
        utils.try_create_feed(feeds);
    }
});
