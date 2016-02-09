let Feed = Backbone.Model.extend({
});
let Feeds = Backbone.Collection.extend({
    model: Feed,
    url: '/reader/api/feeds',
});

export default {Feed, Feeds};
