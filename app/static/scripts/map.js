var map;
var popup;
var queue = [];
var stations = {};
var searchActive = false;
var sortBy;
var markerSource;
const ZOOM_THRESHOLD = 12;
const CENTER_ZOOM = 12;
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

function pushToRequestQueue(options = {}) {
    const center = view.getCenter();
    const coordsTransform = ol.proj.toLonLat(center);
    const lon = coordsTransform[0];
    const lat = coordsTransform[1];

    const extent = map.getView().calculateExtent(map.getSize());
    const left = ol.proj.toLonLat(ol.extent.getBottomLeft(extent));
    const right = ol.proj.toLonLat(ol.extent.getBottomRight(extent));
    const radius = Math.floor(ol.sphere.getDistance(left, right) / 2);

    if (typeof options === 'undefined') options = {}
    options.lat = lat;
    options.lon = lon;
    options.radius = radius;
    queue.push(options);
}

function getNewMarkers() {
    if (queue.length) {
        var request = prepareRequest(queue.pop(), api_url + "/gas_stations");
        sendRequestAndSetNewMarkers(request);
        queue = [];
    };
}

function prepareRequest(options, request_url) {
    var request;
    request = new XMLHttpRequest();
    request_url = request_url + "?";
    for (var key in options) {
        if (options.hasOwnProperty(key)) {
            if (request_url.slice(-1) === "?") {
                request_url = request_url + key + "=" + options[key];
            }
            else {
                request_url = request_url + "&" + key + "=" + options[key];
            }
        }
    }
    request.open('GET', request_url);
    return request;
}

function sendRequestAndSetNewMarkers(request) {
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            setNewMarkers(this);
        }
        if (this.readyState == 4 && this.status == 400) {
            resp = JSON.parse(request.responseText);
            alert("Nieprawidłowe zapytanie: " + resp.message);
        }
    };
    request.send();
}

function canSearch() {
    const name = document.getElementsByName("gas_station_name")[0].value;
    return (name.length > 0);
}

function canSearchAdv() {
    // Czy to potrzebne???
    const name = document.getElementsByName("gs_name")[0].value;
    const min_price = document.getElementsByName("gs_price_min")[0].value;
    const max_price = document.getElementsByName("gs_price_max")[0].value;
    const fuel = document.getElementsByName("gs_fuel")[0].value;
    const min_rate = document.getElementsByName("gs_rate_min")[0].value;
    const max_rate = document.getElementsByName("gs_rate_max")[0].value;
    return ((fuel.length > 0) || (name.length > 0) || (min_price.length > 0) || (max_price.length > 0)
        || (min_rate.length > 0) || (max_rate.length > 0));
}

function searchStringChanged() {
    if (canSearch()) {
        document.getElementById("close-search-button").style.display = "";
    }
    else {
        document.getElementById("close-search-button").style.display = "";
    }
}

function simpleSearch() {
    clearMarkers();

    options = {}
    const name = document.getElementsByName("gas_station_name")[0].value;
    if (name.length > 0) options.name = name;

    pushToRequestQueue(options);
    getNewMarkers();
    searchActive = true;
}

function endSearch() {
    document.getElementsByName("gas_station_name")[0].value = "";
    document.getElementById("close-search-button").style.display = "none";
    document.getElementById("search-results-box").style.display = "none";

    if (searchActive) {
        clearMarkers();
        searchActive = false;
    }
}

function advancedSearch() {
    clearMarkers();

    options = {}
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
    if (document.getElementById("sort-dropdown") !== null)
    {
        sortBy = document.getElementById("sort-dropdown").value;
        const temp = sortBy.split(";");
        options.sort_by = temp[0];
        options.sort_direction = temp[1];
    }

    pushToRequestQueue(options);
    getNewMarkers();

    var request = prepareRequest(options, "/gas_stations");
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("search-results-box").style.display = "";
            document.getElementById("search-results-box").innerHTML = this.responseText;
            if (sortBy.length>0)
            {
                document.getElementById("sort-dropdown").value = sortBy;
            }
        }
    };
    request.send();
    searchActive = true;
}

function showHideAdvancedSearchBox() {
    // pokazuje okienko wyszukiwania zaawansowanego
    if (document.getElementById("search-box").style.display === "none") {
        document.getElementById("advanced-search-button").innerHTML = "&#11205;";
        document.getElementById("search-box").style.display = "";
        document.getElementsByName("gas_station_name")[0].disabled = true;
        document.getElementById("search-button").disabled = true;
        if (document.getElementById("search-box").innerHTML.length === 0) {
            var request = new XMLHttpRequest();
            request.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("search-box").innerHTML = this.responseText;
                }
            };
            request.open('GET', "/searchbox");
            request.send();
        }
    }
    // chowa okienko wyszukiwania zaawansowanego
    else {
        document.getElementById("search-box").style.display = "none";
        document.getElementById("advanced-search-button").innerHTML = "&#11206;";
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
        document.getElementById("show-comment-down").style.display = '';
        document.getElementById("show-comment-up").style.display = 'none';
    }
    else {
        document.getElementsByClassName("comment-form")[0].style.display = 'none';
        document.getElementById("show-comment-down").style.display = 'none';
        document.getElementById("show-comment-up").style.display = '';
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

function centerOnGasStation(lon, lat) {
    map.getView().setCenter(ol.proj.transform([lon, lat], 'EPSG:4326', 'EPSG:3857'));
    map.getView().setZoom(CENTER_ZOOM);
}

function refreshGasStationInfo() {
    if (document.getElementById("iframe").contentDocument.body.innerHTML.length > 0) {
        document.getElementById("big-popup").innerHTML = document.getElementById("iframe").contentDocument.body.innerHTML;
        document.getElementById("iframe").contentDocument.body.innerHTML = "";
        document.getElementById("rate").value = "";
        document.getElementById("comment").value = "";
    }
}
