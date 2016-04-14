let SubCollectionMixin = {
    parse(data) {
        if (this.isNew() && _.has(data, this.idAttribute) && this.sub_collection) {
            let {name, SubCollection} = this.sub_collection;
            this[name] = new SubCollection();
            this._setup_sub_events(name, this[name]);
            let base = this.url() + `/${data.id}`;
            this[name].url = `${base}/${name}`;
            this[name].parent_model = this;
        }
        return Backbone.Model.prototype.parse.apply(this, arguments);
    },
    _setup_sub_events(name, collection) {
        this.listenTo(collection, 'sync', ()=> {
            this.trigger(`${name}:sync`, collection);
        });
    },
};

let Entry = Backbone.Model.extend({
    defaults: {
        'title': '',
        'summary': '',
        'content': '',
        'published': '',
        'url': '',
        'is_starred': false,
    },
    isNewEntry() {
        // let published_date = this.get('published');
        // let today = new Date();
        // return today.getYear() == published_date.getYear() &&
        //     today.getMonth() == published_date.getMonth() &&
        //     today.getDate() == published_date.getDate();
        return !this.get('is_read');
    },
    toggleStar() {
        this.save({is_starred: !this.get('is_starred')});
    },
    parse(data) {
        if (data.published) {
            data.published = new Date(data.published);
        }
        return data;
    },
    content() {
        if ($(this.get('content')).text()) {
            return this.get('content');
        } else {
            return this.get('summary');
        }
    },
    save() {
        if (global_context.authed) {
            this.constructor.__super__.save.apply(this, arguments);
        }
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

let Feed = Backbone.Model.extend({
    sub_collection: {
        SubCollection: Entries,
        name: 'entries',
    },
    refresh() {
        this.fetch({data: {refresh: true}}).then(()=>this.entries.fetch());
    },
    save() {
        if (global_context.authed) {
            this.constructor.__super__.save.apply(this, arguments);
        }
    }
}).extend(SubCollectionMixin);

let Feeds = Backbone.Collection.extend({
    model: Feed,
    url: '/reader/api/feeds',
});

let Category = Backbone.Model.extend({
    sub_collection: {
        SubCollection: Feeds,
        name: 'feeds',
    },
    defaults: {
        name: 'default'
    },
}).extend(SubCollectionMixin);

let Categories = Backbone.Collection.extend({
    model: Category,
    url: '/reader/api/categories',
});

let categories = new Categories();
export {categories};
