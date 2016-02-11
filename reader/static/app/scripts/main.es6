import './setup';
import {feeds} from './models';
import {AddFeedView, MiddleLayout} from './ui';


let app = new Marionette.Application;
app.addRegions({
    top_region: '#top_region',
    middle_region: '#middle_region',
    bottom_region: '#bottom_region',
});

app.on('start', ()=> {
    app.getRegion('top_region').show(new AddFeedView);
    app.getRegion('middle_region').show(new MiddleLayout);
    feeds.fetch();
});

$(()=>app.start());
