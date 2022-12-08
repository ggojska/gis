var map;
var mercator = new OpenLayers.Projection("EPSG:900913");
var wgs84 = new OpenLayers.Projection("EPSG:4326");
var apiKey = "ApTJzdkyN1DdFKkRAE6QIDtzihNaf6IWJsT-nQ_2eMoO4PN__0Tzhl2-WgJtXFSp";
var options = {
    projection: mercator,
    controls: [],
    displayProjection: wgs84
};

function init() {
    map = new OpenLayers.Map("mapa", options);

    var bingRoads = new OpenLayers.Layer.Bing({
        name: 'drogi',
        key: apiKey,
        type: "Road"
    });
    var bingAerials =
        new OpenLayers.Layer.Bing({
            name: 'satelita',
            key: apiKey,
            type: "Aerial"
        });
    var bingAerialsWithLabels =
        new OpenLayers.Layer.Bing({
            name: 'hybryda',
            key: apiKey,
            type: "AerialWithLabels"
        });
    var osm = new OpenLayers.Layer.OSM("Simple OSM Map");
    map.addLayers([osm, bingRoads, bingAerials, bingAerialsWithLabels]);

    // Dodawanie kontrolki do wybierania warstw
    var layerSwitcher = new OpenLayers.Control.LayerSwitcher();
    var zoomBar = new OpenLayers.Control.PanZoomBar();
    var overview = new OpenLayers.Control.OverviewMap();
    var scaleLine = new OpenLayers.Control.ScaleLine();
    var kbDefaults = new OpenLayers.Control.KeyboardDefaults();
    var mousePos = new OpenLayers.Control.MousePosition();

    map.addControl(layerSwitcher);
    map.addControl(zoomBar);
    map.addControl(overview);
    map.addControl(scaleLine);
    map.addControl(kbDefaults);
    map.addControl(mousePos);

    map.displayProjection = wgs84;

    // Ustawianie wyśrodkowania na podane wspołrzedne + transofmacja wgs84 -> mercator
    map.setCenter(new OpenLayers.LonLat(18.64542, 54.34766).transform(wgs84, mercator), 7);
}