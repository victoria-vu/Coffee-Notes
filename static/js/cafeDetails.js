'use strict';

// Add or Remove Cafe from "My Cafes" on Cafe Details Page
const myCafeSubmitButton = document.querySelector('#bookmark-cafe');

myCafeSubmitButton.addEventListener('submit', (evt) => {
    evt.preventDefault();

    const myCafeButton = document.querySelector('#bookmark-button');
    if (myCafeButton.innerHTML === 'Add to My Cafes') {
        const formInput = {
            cafe_id: document.querySelector('#cafe-id').value
        };

        fetch(`/cafe/${formInput.cafe_id}/mycafes`, {
            method: 'POST',
            body: JSON.stringify(formInput),
            headers: {
                'Content-Type': 'application/json',
            },
        })

        .then((response) => response.text())
        .then((myCafeStatus) => {
            document.querySelector('#bookmark-button').innerHTML = 'Remove from My Cafes';
            document.querySelector('#bookmark-status').innerHTML = myCafeStatus;
            document.querySelector('#bookmark-button').disabled = true;
            setTimeout(function() {
                document.querySelector('#bookmark-status').innerHTML = '';
                document.querySelector('#bookmark-button').disabled = false;
            }, 3000);
        }) 

    } else if (myCafeButton.innerHTML === 'Remove from My Cafes') {
            const formInput = {
                cafe_id: document.querySelector('#cafe-id').value
            };
    
        fetch(`/cafe/${formInput.cafe_id}/mycafes`, {
            method: 'POST',
            body: JSON.stringify(formInput),
            headers: {
                'Content-Type': 'application/json',
            },
        })
    
        .then((response) => response.text())
        .then((myCafeStatus) => {
            document.querySelector('#bookmark-button').innerHTML = 'Add to My Cafes';
            document.querySelector('#bookmark-status').innerHTML = myCafeStatus;
            document.querySelector('#bookmark-button').disabled = true;
            setTimeout(function() {
                document.querySelector('#bookmark-status').innerHTML = '';
                document.querySelector('#bookmark-button').disabled = false;
            }, 3000);
        });
    }}
);

// Remove Review from Cafe Details Page
const deleteReviewButton = document.querySelector('#delete-review');

if (deleteReviewButton) {
    deleteReviewButton.addEventListener('submit', (evt) => {
        evt.preventDefault();

        const formInput = {
            cafe_id: document.querySelector('#cafe-id').value
        };

        fetch(`/cafe/${formInput.cafe_id}/removereview`, {
            method: 'POST',
            body: JSON.stringify(formInput),
            headers: {
                'Content-Type': 'application/json',
            },
        })

        .then((response) => response.text())
        .then((reviewStatus) => {
            document.querySelector('#customer-review').remove()
            document.querySelector('#remove-review-status').innerHTML = reviewStatus;
            setTimeout(function() {
                window.location.reload();
            }, 4000);
        });
    });
};

// Google Maps API
function initMap() {

    const cafeCoords = {
        lat: Number(document.querySelector('#map-lat').value),
        lng: Number(document.querySelector('#map-lng').value),
    };

    const map = new google.maps.Map(document.querySelector('#map'), {
        center: cafeCoords,
        zoom: 13.1,
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

    const cafeName = document.querySelector('#cafe-name').innerHTML

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

    const cafeInfoContent = `<h4>${cafeName}<h/h4>`

    cafeMarker.addListener('click', () => {
        cafeInfo.setContent(cafeInfoContent)
        cafeInfo.open(map, cafeMarker)
    });

};  

// Edit Review on Details Page
const editButton = document.querySelector('#edit-btn');

const form = document.querySelector('#edit-form');

if (form) {
    form.hidden = true;
}

if (editButton) {
    editButton.addEventListener('click', () => {
        
        if (form.hidden === true) {
            form.hidden = false;
            editButton.innerHTML = "Close Edit Review";
        } else if (form.hidden === false) {
                form.hidden = true;
                editButton.innerHTML = "Edit Review";
        }
    });
}

