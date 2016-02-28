import {categories} from './models';
import * as utils from './utils';
import {default as feed_tpl} from 'templates/feed';
import {default as entry_tpl} from 'templates/entry';
import {default as category_tpl} from 'templates/category';
import {default as top_region_tpl} from 'templates/top_region';
import {default as categories_manager_tpl} from 'templates/categories_manager';
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
    modelEvents: {
        'selected': 'selected'
    },
    selected() {
        this.model.entries.fetch();
        this.$el.addClass('selected');
        this.triggerMethod('feed:selected');
    },
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


/**
 * feeds manager is a heirachical structure containing categries of feeds
 */

let CategoryView = Marionette.ItemView.extend({
    template: category_tpl,
    tagName: 'li',
    className: 'category',
    selected() {
        this.model.feeds.fetch({reset: true});
        this.ui.expander.removeClass('collapsed');
    },
    ui: {
        'expander': '.expander',
    },
    modelEvents: {
        'feeds:sync': 'render',
    },
    events: {
        'click .feed': 'feedSelected',
        'click @ui.expander': 'expand',
    },
    hideFeeds() {
        this.$('.feeds').remove();
        this.ui.expander.addClass('collapsed');
    },
    expand(ev) {
        let expand_it = $(ev.currentTarget).is('.collapsed');
        if (expand_it) {
            this.selected();
        } else {
            this.hideFeeds();
        }
    },
    feedSelected(ev) {
        let feed_id = $(ev.currentTarget).data('id');
        let feed = this.model.feeds.get(feed_id);
        this.triggerMethod('feed:selected', feed);
    },
    templateHelpers() {
        return {
            'feeds': this.model.feeds.toJSON(),
        };
    }
});

let CategoriesManager = Marionette.CompositeView.extend({
    template: categories_manager_tpl,
    childViewContainer: '.categories',
    childView: CategoryView,
    className: 'categories-manager',
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
        'star': '.title-and-time span:first-child',
        'title': '.title',
    },
    events: {
        'click @ui.title': 'openEntry',
        'click @ui.star': 'toggleStar',
    },
    modelEvents: {
        'change:is_starred': 'updateStar',
    },
    updateStar() {
        if (this.model.get('is_starred')) {
            this.ui.star.html('&#9733;');
        } else {
            this.ui.star.html('&#9734;');
        }
    },
    toggleStar() {
        this.model.toggleStar();
    },
    openEntry() {
        if (this.$el.is('.open')) {
            this.$el.removeClass('open');
            return;
        }

        this.ui.entry_content.html(this.model.content());
        this.$el.addClass('open');
    },
    onRender() {
        if (this.model.isNewEntry()) {
            this.$el.addClass('new');
        }
    }
});


let EntriesManagerView = Marionette.CompositeView.extend({
    template: entries_manager_tpl,
    childViewContainer: '.entries',
    childView: EntryView,
    className: 'entries-manager',
    initialize() {
        this.collection.fetch({reset: true});
    },
    ui: {
        'refresh_btn': '.js-refresh-feed',
        'delete_btn': '.js-delete-feed',
    },
    events: {
        'click @ui.delete_btn': 'deleteFeed',
        'click @ui.refresh_btn': 'refreshFeed',
    },
    collectionEvents: {
        'sync' () {this.ui.refresh_btn.prop('disabled', false);}
    },
    deleteFeed() {
        this.triggerMethod('feed:delete');
    },
    refreshFeed() {
        this.ui.refresh_btn.prop('disabled', true);
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
        'feed:delete': 'deleteFeed',
    },
    deleteFeed(childView) {
        let feed = childView.model;
        feed.destroy({success: ()=> toastr.success(feed.get('title') + ' is deleted.')});
        if (feeds.isEmpty()) {
            this.getRegion('right').empty();
        } else {
            feeds.first().trigger('selected'); 
        }
    },
    showEntries(childView, feed) {
        let selected_feed = feed;
        this.getRegion('right').show(new EntriesManagerView({
            model: selected_feed,
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
        this.getRegion('left').show(new CategoriesManager({
            collection: categories,
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
    },
    templateHelpers() {
        return {
            authed
        };
    },
});
