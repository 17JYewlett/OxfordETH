let map;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 51.752, lng: -1.2577 }, // Oxford Coordinates
        zoom: 13,
        styles: [
            {
                featureType: "poi",
                elementType: "labels",
                stylers: [{ visibility: "off" }]
            }
        ]
    });

    const searchBox = new google.maps.places.SearchBox(document.getElementById("searchBox"));
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(document.getElementById("searchBox"));

    searchBox.addListener("places_changed", () => {
        const places = searchBox.getPlaces();
        if (places.length === 0) return;

        const place = places[0];
        map.setCenter(place.geometry.location);
        map.setZoom(15);

        new google.maps.Marker({
            map,
            position: place.geometry.location
        });
    });

    addCourtMarkers();
}

function addCourtMarkers() {
    const courtLocations = [
        { lat: 51.7519, lng: -1.2578, name: "Oxford Court 1" },
        { lat: 51.7533, lng: -1.2599, name: "Oxford Court 2" },
        { lat: 51.7547, lng: -1.2610, name: "Oxford Court 3" }
    ];

    courtLocations.forEach((court) => {
        new google.maps.Marker({
            position: { lat: court.lat, lng: court.lng },
            map,
            title: court.name
        });
    });
}