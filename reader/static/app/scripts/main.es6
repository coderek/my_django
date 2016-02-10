import './setup';
import {feeds} from './models';
import './ui';


let app = new Marionette.Application;
app.on('start', ()=> feeds.fetch());

$(function () {
    app.start();
});
