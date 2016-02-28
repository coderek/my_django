import './setup';
import {categories} from './models';
import {ReaderLayout} from './ui';

let ReaderApp = Marionette.Application;
let app = new ReaderApp;
app.rootView = new ReaderLayout;

app.on('start', ()=> {
    app.rootView.render();
    categories.fetch({reset: true});
});

$(()=>app.start());
