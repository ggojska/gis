var map;
var popup;
var queue = [];
var stations = {};
var searchActive = false;
var markerSource;
const ZOOM_THRESHOLD = 12;
const SEND_REQ_DELAY = 2300;
const api_url = "/api/v1";
const basemapId = "ArcGIS:Navigation";
const apiKey = "AAPK456a42556512432bb3e96e0666ce3280EPnsoKrYftXZyA9Sx3Sr-htoFcbRlAbkZgt0oEfJHA34FlD4dpmazYT_apSD0CC5";
var authentication;
var basemapURL;

var point = 0;
var point2 = 0;
var pointToSave = 1;
var showRoute = false;

let currentStep = "start";
let startCoords, endCoords;

const geojson = new ol.format.GeoJSON({
    defaultDataProjection: "EPSG:4326",
    featureProjection: "EPSG:3857"
  });

function init() {

    map = new ol.Map({
        target: document.getElementById("mapa"),
        projection: new ol.proj.Projection("EPSG:4326"),
        view: new ol.View({
            center: ol.proj.fromLonLat([18.64542, 54.34766]),
            zoom: 10
        })
    });

    authentication = arcgisRest.ApiKeyManager.fromKey(apiKey);
    basemapURL = "https://basemaps-api.arcgis.com/arcgis/rest/services/styles/" + basemapId + "?type=style&token=" + apiKey;

    olms(map, basemapURL)
    .then(function (map) {
        addCircleLayers();
        addRouteLayer();
        //addMarkersLayer();
      });


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
        if (isBigPopupDisplayed()) 
        {
            document.getElementById("big-popup").style.display = "none";
        }
        else
        {
            const coordinates = ol.proj.transform(evt.coordinate, "EPSG:3857", "EPSG:4326");
            const point = {
                type: "Point",
                coordinates
            };

            if (currentStep === "start") 
            {
                startLayer.setSource(
                    new ol.source.Vector({
                    features: geojson.readFeatures(point)
                    })
                );
                startCoords = coordinates;
                if (endCoords) {
                    endCoords = null;
                    endLayer.getSource().clear();
        
                  }

                currentStep = "end";
            } 

            else 
            {
                endLayer.setSource(
                    new ol.source.Vector({
                    features: geojson.readFeatures(point)
                    })
                );
                endCoords = coordinates;
                currentStep = "start";
                updateRoute(startCoords, endCoords);
            }

            if(showRoute)
            {
                setRouteMarkers();
                updateRoute();
            }
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
        if (this.readyState == 4 && this.status == 400) {
            resp = JSON.parse(request.responseText);
            alert("Nieprawidłowe zapytanie: " + resp.message);
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

function simpleSearch() {
    clearMarkers();

    options = {}
    const name = document.getElementsByName("gas_station_name")[0].value;
    if (name.length > 0) options.name = name;

    pushToRequestQueue(options);
    getNewMarkers();
    searchActive = true;
    document.getElementById("cancel-search").style.display = "";
}

function endSearch() {
    document.getElementsByName("gas_station_name")[0].value = "";
    document.getElementById("close-search-button").style.display = "none";
    document.getElementById("cancel-search").style.display = "none";

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

    pushToRequestQueue(options);
    getNewMarkers();
    searchActive = true;
    document.getElementById("cancel-search").style.display = "";
}

function showHideAdvancedSearchBox() {
    // pokazuje okienko wyszukiwania zaawansowanego
    if (document.getElementById("search-box").style.display === "none") {
        document.getElementById("advanced-search-button").innerHTML = "&#11205;";
        document.getElementById("search-box").style.display = "";
        document.getElementsByName("gas_station_name")[0].disabled = true;
        document.getElementById("search-button").disabled = true;
        if (document.getElementById("search-box").innerHTML.length === 0){
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
}

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

function findRoute() {
    showRoute == false ? showRoute = true : showRoute = false
}

function updateRoute() {

    const authentication = arcgisRest.ApiKeyManager.fromKey(apiKey);

    arcgisRest

      .solveRoute({
        stops: [startCoords, endCoords],
        authentication
      })
      .then((response) => {
          console.log(response.directions[0].summary.totalLength);
          
          routeLayer.setSource(
              new ol.source.Vector({
                  features: geojson.readFeatures(response.routes.geoJson)
                })
                );
                
            })
            
            .catch((error) => {
                alert("There was a problem using the geocoder. See the console for details.");
                console.error(error);
            });


            
    const directionsHTML = response.directions[0].features.map((f) => f.attributes.text).join("<br/>");
    document.getElementById("directions").innerHTML = directionsHTML;
    document.getElementById("directions").style.display = "block";

  }

function setRouteMarkers() 
{
    markers = [];

    var point1 = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([point.x, point.y])),
        id: 1
    });

    var point2 = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([point2.x, point2.y])),
        id: 2
    });

    markers.push(point1);
    markers.push(point2);

    if (typeof markerSource === 'undefined') markerSource = new ol.source.Vector();
    markerSource.addFeatures(markers);

    var markerLayer = new ol.layer.Vector({
        source: markerSource,
    });
    map.addLayer(markerLayer);
}

function addRouteLayer() 
{
    routeLayer = new ol.layer.Vector({
      style: new ol.style.Style({
        stroke: new ol.style.Stroke({ color: "hsl(205, 100%, 50%)", width: 4, opacity: 0.6 })
      })
    });

    map.addLayer(routeLayer);
  }

function addMarkersLayer()
{
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

let startLayer, endLayer, routeLayer, markerLayer;
function addCircleLayers() 
{

    startLayer = new ol.layer.Vector({
      style: new ol.style.Style({
        image: new ol.style.Circle({
          radius: 6,
          fill: new ol.style.Fill({ color: "white" }),
          stroke: new ol.style.Stroke({ color: "black", width: 2 })
        })
      })
    });
    map.addLayer(startLayer);

    endLayer = new ol.layer.Vector({
      style: new ol.style.Style({
        image: new ol.style.Circle({
          radius: 7,
          fill: new ol.style.Fill({ color: "black" }),
          stroke: new ol.style.Stroke({ color: "white", width: 2 })
        })
      })
    });

    map.addLayer(endLayer);
}