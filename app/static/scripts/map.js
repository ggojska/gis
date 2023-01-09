var map;
var popup;
var queue = [];
var stations = {};
var searchActive = false;
var markerSource;
const ZOOM_THRESHOLD = 12;
const SEND_REQ_DELAY = 2300;
const api_url = "/api/v1";

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
            if (!searchActive) pushToRequestQueue();
            setTimeout(function () {
                getNewMarkers();
            }, SEND_REQ_DELAY);
        }
        else {
            if (!searchActive) clearMarkers();
        };
    });

    map.on("click", function (evt) {
        if (isBigPopupDisplayed()) {
            document.getElementById("big-popup").style.display = "none";
        }
    });

    map.on("pointermove", function (evt) {
        if (evt.dragging) return;
        displayGasStationPopup(evt);
    });

    map.on("movestart", function () {
        queue = [];
    });
};

function pushToRequestQueue() {
    var center = view.getCenter();
    var coordsTransform = ol.proj.toLonLat(center);
    var lon = coordsTransform[0];
    var lat = coordsTransform[1];

    var extent = map.getView().calculateExtent(map.getSize());
    var left = ol.proj.toLonLat(ol.extent.getBottomLeft(extent));
    var right = ol.proj.toLonLat(ol.extent.getBottomRight(extent));
    var radius = Math.floor(ol.sphere.getDistance(left, right) / 2);
    options = { "lat": lat, "lon": lon, "radius": radius }

    const name = document.getElementsByName("gas_station_name")[0].value;
    if (name.length > 0) options.name = name;
    const name2 = document.getElementsByName("gs_name")[0].value;
    if (name2.length > 0) options.name = name2;
    const min_price = document.getElementsByName("gs_price_min")[0].value;
    if (min_price.length > 0) options.min_price = min_price;
    const max_price = document.getElementsByName("gs_price_max")[0].value;
    if (max_price.length > 0) options.max_price = max_price;
    const fuel = document.getElementsByName("gs_fuel")[0].value;
    if (fuel.length > 0) options.fuel = fuel;
    const min_rate = document.getElementsByName("gs_rate_min")[0].value;
    if (min_rate.length > 0) options.min_rate = min_rate;
    const max_rate = document.getElementsByName("gs_rate_max")[0].value;
    if (max_rate.length > 0) options.max_rate = max_rate;

    queue.push(options);
}

function getNewMarkers() {
    if (queue.length) {
        prepareAndSendRequest(queue.pop());
        queue = [];
    };
}

function prepareAndSendRequest(options) {
    var request;
    request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            setNewMarkers(this);
        }
    };
    request_url = api_url + "/gas_stations?lon=" + options.lon + "&lat=" + options.lat + "&radius=" + options.radius
    if ("name" in options) request_url += "&name=" + options.name;
    if ("fuel" in options) request_url += "&fuel=" + options.fuel;
    if ("min_price" in options) request_url += "&min_price=" + options.min_price;
    if ("max_price" in options) request_url += "&max_price=" + options.max_price;
    if ("min_rate" in options) request_url += "&min_rate=" + options.min_rate;
    if ("max_rate" in options) request_url += "&max_rate=" + options.max_rate;
    request.open('GET', request_url);
    request.send();
}

function canSearch() {
    const name = document.getElementsByName("gas_station_name")[0].value;
    return (name.length > 0)
}

function canSearchAdv() {
    const name = document.getElementsByName("gs_name")[0].value;
    const min_price = document.getElementsByName("gs_price_min")[0].value;
    const max_price = document.getElementsByName("gs_price_max")[0].value;
    const fuel = document.getElementsByName("gs_fuel")[0].value;
    const min_rate = document.getElementsByName("gs_rate_min")[0].value;
    const max_rate = document.getElementsByName("gs_rate_max")[0].value;
    return ((fuel.length > 0) || (name.length > 0) || (min_price.length > 0) || (max_price.length > 0)
        || (min_rate.length > 0) || (max_rate.length > 0))
}

function searchStringChanged() {
    if (canSearch()) {
        document.getElementById("close-search-button").style.display = "";
    }
    else {
        document.getElementById("close-search-button").style.display = "";
    }
}

function normalSearch() {
    if (canSearch()) {
        clearMarkers();
        pushToRequestQueue();
        getNewMarkers();
        searchActive = true;
    }
}

function advancedSearch() {
    if (canSearchAdv()) {
        clearMarkers();
        pushToRequestQueue();
        getNewMarkers();
        searchActive = true;
    }
}

function endSearch() {
    document.getElementsByName("fuel_name")[0].value = "";
    document.getElementsByName("gas_station_name")[0].value = "";
    document.getElementById("close-search-button").style.display = "none";

    if (searchActive) {
        clearMarkers();
        searchActive = false;
    }
}

function showHideAdvancedSearchBox() {
    if (document.getElementById("search-box").style.display === "none") {
        // show advanced search box
        document.getElementById("search-box").style.display = "";
        document.getElementById("advanced-search-button").innerHTML = "x";
        document.getElementsByName("gas_station_name")[0].disabled = true;
        document.getElementById("search-button").disabled = true;
        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("search-box").innerHTML = this.responseText;
            }
        };
        request.open('GET', "/searchbox");
        request.send();
    }
    else {
        // hide advanced search box
        document.getElementById("search-box").style.display = "none";
        document.getElementById("advanced-search-button").innerHTML = "...";
        document.getElementsByName("gas_station_name")[0].disabled = false;
        document.getElementById("search-button").disabled = false;
    }
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

function displayGasStationPopup(evt) {
    var myFeature;

    map.forEachFeatureAtPixel(evt.pixel, function (feature) {
        myFeature = feature;
    });

    if (typeof myFeature !== 'undefined' && !isBigPopupDisplayed()) {
        var id = myFeature.values_.id;

        popup.setPosition(evt.coordinate);
        map.getTarget().style.cursor = "pointer";
        map.getTarget().onclick = function () {
            displayGasStationInfo(id);
        };

        if (id in stations) {
            document.getElementById("popup").innerHTML = stations[id];
            return;
        }

        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                stations[id] = this.responseText;
                document.getElementById("popup").innerHTML = this.responseText;
            }
        };
        request.open('GET', "/gas_stations/" + id + "/popup");
        request.send();

    } else {
        popup.setPosition(undefined);
        map.getTarget().style.cursor = "";
        map.getTarget().onclick = function () {
            // pass
        };
    }
};

function displayGasStationInfo(gasStationId) {
    if (!isBigPopupDisplayed()) {
        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("big-popup").style.display = "flex";
                document.getElementById("big-popup").innerHTML = this.responseText;
            }
        };
        request.open('GET', "/gas_stations/" + gasStationId + "/comments");
        request.send();
    }
}

function hideGasStationInfo() {
    document.getElementById("big-popup").style.display = "none";
    map.getTarget().style.cursor = "";
    map.getTarget().onclick = function () {
        // pass
    };
}

function isBigPopupDisplayed() {
    return (document.getElementById("big-popup").style.display !== "none")
}

function showAddComment() {
    if (document.getElementsByClassName("comment-form")[0].style.display === 'none') {
        document.getElementsByClassName("comment-form")[0].style.display = '';
    }
    else {
        document.getElementsByClassName("comment-form")[0].style.display = 'none';
    }
}

function deleteComment(gasStationId, commentId) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("big-popup").style.display = "flex";
            document.getElementById("big-popup").innerHTML = this.responseText;
        }
    };
    request.open('POST', "/gas_stations/" + gasStationId + "/comments/" + commentId + "/delete");
    request.send();
}

function refreshGasStationInfo() {
    console.log("refreshGasStationInfo");
    if (document.getElementById("iframe").innerHTML.length > 0) {
        document.getElementById("big-popup").innerHTML = document.getElementById("iframe").innerHTML;
    }
}
