var map;
var popup;
var queue = [];
var stations = {};
var markerSource;
const ZOOM_THRESHOLD = 12;
const WAIT_UNTIL_SEND_REQ = 2750;
const api_url = "/api/v1/";

function init() {

    map = new ol.Map({
        target: document.getElementById("mapa"),
        projection: new ol.proj.Projection("EPSG:4326"),
        view: new ol.View({
            center: ol.proj.fromLonLat([18.64542, 54.34766]),
            zoom: 10
        })
    });

    var osm = new ol.layer.Tile({
        source: new ol.source.OSM()
    });

    map.getLayers().insertAt(0, osm);

    var popupBody = document.getElementById('popup');
    popup = new ol.Overlay({
        element: popupBody,
    });
    map.addOverlay(popup);

    map.on("moveend", function () {
        view = map.getView()
        var zoom = view.getZoom();
        if (zoom > ZOOM_THRESHOLD) {
            var center = view.getCenter();
            var coordsTransform = ol.proj.toLonLat(center);
            var lon = coordsTransform[0];
            var lat = coordsTransform[1];

            var extent = map.getView().calculateExtent(map.getSize());
            var left = ol.proj.toLonLat(ol.extent.getBottomLeft(extent));
            var right = ol.proj.toLonLat(ol.extent.getBottomRight(extent));
            var radius = Math.floor(ol.sphere.getDistance(left, right) / 2);
            queue.push([lon, lat, radius]);

            setTimeout(function () {
                getNewMarkers();
            }, WAIT_UNTIL_SEND_REQ);
        }
        else {
            clearMarkers();
        };
    });

    map.on("pointermove", function (evt) {
        if (evt.dragging) return;
        displayFeatureInfo(evt);
    });

    map.on("movestart", function () {
        queue = [];
    });
}

function getNewMarkers() {
    if (queue.length) {
        elem = queue.pop();
        queue = [];

        var request;
        request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                setNewMarkers(this);
            }
        };
        request.open('GET', api_url + "/gas_stations?lon=" + elem[0] + "&lat=" + elem[1] + "&radius=" + elem[2]);
        request.send();
    };
}

function setNewMarkers(request) {
    json = JSON.parse(request.response);

    clearMarkers();
    markers = [];
    json.gas_stations.forEach(element => {
        var point = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat([element.lon, element.lat])),
            id: element.id
        });

        point.setStyle(
            new ol.style.Style({
                image: new ol.style.Icon({
                    src: element.icon,
                    scale: 1
                })
            })
        );

        markers.push(point);
    });

    if (typeof markerSource === 'undefined') markerSource = new ol.source.Vector();
    markerSource.addFeatures(markers);

    var markerLayer = new ol.layer.Vector({
        source: markerSource,
    });
    map.addLayer(markerLayer);
}

function clearMarkers() {
    if (typeof markerSource !== 'undefined') {
        markerSource.clear();
    }
}

function displayFeatureInfo(evt) {
    var myFeature;

    map.forEachFeatureAtPixel(evt.pixel, function (feature) {
        myFeature = feature;
    });

    if (typeof myFeature !== 'undefined') {
        popup.setPosition(evt.coordinate);
        map.getTarget().style.cursor = "pointer";
        var id = myFeature.values_.id;

        if (id in stations) {
            document.getElementById("popup").innerHTML = getGasStationInfoFromResponse(stations[id]);
            return;
        }

        var request;
        request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                stations[id] = this;
                document.getElementById("popup").innerHTML = getGasStationInfoFromResponse(this);
            }
        };
        request.open('GET', api_url + "/gas_stations/" + id);
        request.send();

    } else {
        popup.setPosition(undefined);
        map.getTarget().style.cursor = "";
    }
};

function getGasStationInfoFromResponse(request) {
    json = JSON.parse(request.response);

    var info = [];
    info.push("<p>Stacja <strong>" + json.name + "</strong></p>")

    var isFuelPriceInfo = json.fuels.length;
    if (isFuelPriceInfo) info.push('<table id="fuel">');
    json.fuels.forEach(fuel => {
        info.push("<tr><td>" + fuel.name + "</td><td><strong>" + fuel.price + "</strong></td></tr>");
    });

    if (isFuelPriceInfo) {
        info.push('</table>')
    }
    else {
        info.push("<p>brak informacji o cenach paliwa</p>");
    }

    return info.join("");
}
