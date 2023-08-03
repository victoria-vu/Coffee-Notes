'use strict';

// Google Maps API
function initMap() {
    const cafeCoords = {
        lat: Number(document.querySelector('#map-lat').value),
        lng: Number(document.querySelector('#map-lng').value),
    };

    // const map creates the WHOLE map
    const map = new google.maps.Map(document.querySelector('#map'), {
        center: cafeCoords,
        zoom: 13.1,
    });

    const cafeName = document.querySelector('#cafe-name').innerHTML

    // const cafeMarker creates a marker to add to the map
    const cafeMarker = new google.maps.Marker({
        position: cafeCoords,
        title: 'Cafe Name',
        icon: {
            url: '/static/img/coffee.png',
            scaledSize: new google.maps.Size(40,40),
        },
        map: map,
    });

    const cafeInfo = new google.maps.InfoWindow();

    const cafeInfoContent = `<h4>${cafeName}</h4>`

    cafeMarker.addListener('click', () => {
        cafeInfo.setContent(cafeInfoContent)
        cafeInfo.open(map, cafeMarker)
    });
};  
