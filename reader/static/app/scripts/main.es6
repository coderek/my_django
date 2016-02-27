import './setup';
import {categories} from './models';
import {TopRegionView, MiddleLayout} from './ui';


let app = new Marionette.Application;
app.addRegions({
    top_region: '#top_region',
    middle_region: '#middle_region',
    bottom_region: '#bottom_region',
});

app.on('start', ()=> {
    app.getRegion('top_region').show(new TopRegionView);
    app.getRegion('middle_region').show(new MiddleLayout);
    categories.fetch({reset: true});
});

$(()=>app.start());
