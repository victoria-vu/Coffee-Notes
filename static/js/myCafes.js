'use strict';

// Remove Cafe Visit on My Cafes Page
const removeBookmarkButton = document.querySelector('#remove-bookmark');

if (removeBookmarkButton) {
removeBookmarkButton.addEventListener('submit', (evt) => {
    evt.preventDefault();

    // Selects the ID of the particular button and pulls the value from it, which is the cafe_id
    const formInput = {
        cafe_id: document.querySelector('#remove-bookmark-id').value
    };

    fetch(`/cafe/${formInput.cafe_id}/removecafebookmark`, {
        method: 'POST',
        body: JSON.stringify(formInput),
        headers: {
            'Content-Type': 'application/json',
        },
    })

    .then((response) => response.text())
    .then((visitStatus) => {
        document.querySelector('#bookmark-cafe-info').remove()
        document.querySelector('#remove-notes').remove()
        document.querySelector('#add-notes').remove()
        document.querySelector('#remove-bookmark').remove()
        document.querySelector('#remove-bookmark-status').innerHTML = visitStatus;
        setTimeout(function() {
            window.location.reload();
         }, 4000);
        });
    });
};


// Google Maps API
function initMap() {
    const map = new google.maps.Map(document.querySelector('#map'), {
        center: {
            lat: 37.601773,
            lng: -122.20287,
        },
        zoom: 11,
        styles: [
            {
                "featureType": "administrative.land_parcel",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "landscape.man_made",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "simplified"
                    },
                    {
                        "lightness": 20
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry",
                "stylers": [
                    {
                        "hue": "#f49935"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "geometry",
                "stylers": [
                    {
                        "hue": "#fad959"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.local",
                "elementType": "geometry",
                "stylers": [
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "road.local",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "transit",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "all",
                "stylers": [
                    {
                        "hue": "#a1cdfc"
                    },
                    {
                        "saturation": 30
                    },
                    {
                        "lightness": 49
                    }
                ]
            }
        ]
    });

    const cafeInfo = new google.maps.InfoWindow();

    fetch('/api/mycafes')
      .then((response) => response.json())
      .then((cafes) => {
        for (const cafe of cafes) {

            const cafeInfoContent = `
            <h1>${cafe.name}</h1>
            <h4>Address:</h4>
            <p>${cafe.address} <br>
            ${cafe.city} ${cafe.state} ${cafe.zip_code}</p>
            <h4>Phone Number:</h4> 
            <p>${cafe.phone}</p>
            `
            
            const cafeMarker = new google.maps.Marker({
                position: {
                    lat: cafe.lat,
                    lng: cafe.lng,
                },
                title: `Cafe Name: ${cafe.name}`,
                icon: {
                    url: '/static/img/coffee.png',
                    scaledSize: new google.maps.Size(40,40),
                },
                map,
            });

            cafeMarker.addListener('click', () => {
                cafeInfo.close();
                cafeInfo.setContent(cafeInfoContent)
                cafeInfo.open(map, cafeMarker)
            });
        }
      })
};  