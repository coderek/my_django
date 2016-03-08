import {categories} from './models';
import * as utils from './utils';

// templates

import {default as new_feed_form_tpl} from 'templates/new_feed_form';
import {default as reader_tpl} from 'templates/reader_layout';
import {default as feed_tpl} from 'templates/feed';
import {default as entry_tpl} from 'templates/entry';
import {default as category_tpl} from 'templates/category';
import {default as top_region_tpl} from 'templates/top_region';
import {default as categories_manager_tpl} from 'templates/categories_manager';
import {default as entries_manager_tpl} from 'templates/entries_manager';
import {default as middle_layout_tpl} from 'templates/middle_layout';

/*
let EmptyFeedsView = Marionette.ItemView.extend({
    template: no_feeds_tpl,
    className: 'empty-view',
    events: {
        'click .js-add-feed': 'create_feed',
    },
    create_feed() {
        this.triggerMethod('feed:create');
    }
});
*/


/**
 * feeds manager is a heirachical structure containing categries of feeds
 */

let CategoryView = Marionette.ItemView.extend({
    template: category_tpl,
    tagName: 'li',
    className: 'category',
    // emptyView: EmptyFeedsView,

    initialize() {
        this.listenTo(this.model.feeds, 'change destroy reset', this.render);
        this.listenTo(this.model.feeds, 'selected', this.feedSelected);
    },
    selected() {
        this.model.feeds.fetch({reset: true});
        this.ui.expander.removeClass('collapsed');
    },
    ui: {
        'expander': '.expander',
    },
    modelEvents: {
        'feeds:sync': 'render',
        'selected': 'showDefaultView',
    },
    events: {
        'click .feed': 'feedSelected',
        'click @ui.expander': 'expand',
    },
    triggers: {
        'click .js-add-feed': 'feed:create',
    },
    showDefaultView() {
        this.model.feeds.first().selected();
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
    feedSelected(ev_or_model) {
        var feed_id;
        if (ev_or_model instanceof Backbone.Model) {
            feed_id = ev_or_model.id;
        } else {
            feed_id = $(ev_or_model.currentTarget).data('id');
        }
        let feed = this.model.feeds.get(feed_id);
        this.triggerMethod('feed:selected', feed);
    },
    templateHelpers() {
        return {
            'feeds': this.model.feeds.map((f) => {
                return _.extend(f.toJSON(), {
                    'count': f.get('count') > 99 ? '99+' : f.get('count') + '',
                });
            }),
        };
    }
});

let CategoriesManager = Marionette.CompositeView.extend({
    template: categories_manager_tpl,
    childViewContainer: '.categories',
    childView: CategoryView,
    className: 'categories-manager',
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
        },
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
        'change:is_read': 'updateRead',
    },
    updateStar() {
        if (this.model.get('is_starred')) {
            this.ui.star.html('&#9733;');
        } else {
            this.ui.star.html('&#9734;');
        }
    },
    updateRead() {
        if (this.model.isNewEntry()) {
            this.$el.removeClass('new');
        } else {
            this.$el.addClass('new');
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
        if (this.model.isNewEntry()) {
            this.model.save(
                {is_read: true},
                {
                    patch: true,
                    wait: true,
                    success: ()=> this.model.collection.parent_model.fetch()
                }
            );
        }
    },
    onRender() {
        this.updateRead();
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

let MiddleLayout = Marionette.LayoutView.extend({
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
        'feed:create'() {
            this.triggerMethod('feed:create');
        }
    },
    deleteFeed(childView) {
        let feed = childView.model;
        let feeds = feed.collection;
        feed.destroy({success: ()=> toastr.success(feed.get('title') + ' is deleted.')});
        if (feeds.isEmpty()) {
            this.getRegion('right').empty();
        } else {
            var first = feeds.first();
            first.trigger('selected', first);
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


let TopRegionView = Marionette.ItemView.extend({
    template: top_region_tpl,
    ui: {
        'add_button': '#add_feed',
    },
    triggers: {
        'click @ui.add_button': 'feed:create',
    },
    templateHelpers() {
        return {
            authed
        };
    },
});


let PopupMixin = {
    getTemplate() {
        let originalTemplate = this.constructor.__super__.getTemplate();
        return () => {
            return `<div class='popup'>${originalTemplate.call(this)}</div>`;
        };
    },
};


let NewFeedForm = Marionette.ItemView.extend({
    template: new_feed_form_tpl,
    events: {
        'submit form': 'submitForm',
    },
    onShow() {
        this.$('input').focus();
    },
    submitForm(ev) {
        let data = this.$('form').serializeObject();
        let category = categories.get(data['category']);
        this.$('input, button').prop('disabled', true);
        category.feeds.create({url: data['new_feed_url']}, {
            wait: true,
            success: (m)=> {
                this.triggerMethod('feed:added');
                toastr.success(`"${m.get('title')}" is added!`);
                this.$('input, button').prop('disabled', false);
            },
            error: ()=> {
                this.$('input, button').prop('disabled', false);
            },
        });
        return false;
    }
}).extend(PopupMixin);

export let ReaderLayout = Marionette.LayoutView.extend({
    el: '#reader',
    template: reader_tpl,
    regions: {
        popup: '#popup_region',
        top: '#top_region',
        middle: '#middle_region',
        bottom: '#bottom_region',
    },

    events: {
        'click #popup_region'(ev) {
            if ($(ev.target).parent().is('#popup_region'))
                this.getRegion('popup').empty();
        }
    },

    onRender() {
        this.getRegion('top').show(new TopRegionView);
        this.getRegion('middle').show(new MiddleLayout);
    },

    childEvents: {
        'feed:create': 'showCreateFeedView',
        'feed:added': 'closeCreateFeedView',
    },
    closeCreateFeedView() {
        this.getRegion('popup').empty();
    },
    showCreateFeedView() {
        this.getRegion('popup').show(new NewFeedForm);
    },
});

