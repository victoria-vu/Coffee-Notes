'use strict';

// Remove Cafe Visit on My Cafes Page
const removeBookmarkButtons = document.querySelectorAll('.remove-bookmark');

if (removeBookmarkButtons) {
    for (const button of removeBookmarkButtons) {
        button.addEventListener('submit', (evt) => {
            evt.preventDefault();

            const formInput = {
                cafe_id: button.id
            };

            fetch(`/mycafes/${formInput.cafe_id}/removecafebookmark`, {
                method: 'POST',
                body: JSON.stringify(formInput),
                headers: {
                    'Content-Type': 'application/json',
                },
            })

            .then((response) => response.text())
            .then((visitStatus) => {
                document.querySelector(`#bookmark-${formInput.cafe_id}`).remove()
                document.querySelector('#remove-bookmark-status').innerHTML = visitStatus;
                setTimeout(function() {
                    document.querySelector('#remove-bookmark-status').innerHTML = '';
                }, 3000);
            });
        });
    };
};

// Edit Notes on My Cafes Page
const editButtons = document.querySelectorAll('.edit-btn');

const forms = document.querySelectorAll('.edit-form');

// Hides all forms
if (forms) {
    for (const form of forms) { 
    form.hidden = true;
    }
}

if (editButtons) {
    for (const editButton of editButtons) {
     
        editButton.addEventListener('click', () => {
            // formID = edit-note-{{ note.note_id }}
            const formID = editButton.id.replace('btn', 'note');
            // Selects the correct form
            const form = document.querySelector(`#${formID}`)

                if (form.hidden === true) {
                    form.hidden = false;
                    editButton.innerHTML = "Close Edit Note";
                } else if (form.hidden === false) {
                        form.hidden = true;
                        editButton.innerHTML = "Edit Note";
                }
        });
    }
}


// Remove a Cafe Note on My Cafes Page
const removeNoteButtons = document.querySelectorAll('.remove-note');

if (removeNoteButtons) {
    for (const button of removeNoteButtons) {
        button.addEventListener('submit', (evt) => {
            evt.preventDefault();

            const formInput = {
                note_id: button.id
            };

            fetch(`/mycafes/${formInput.note_id}/removenote`, {
                method: 'POST',
                body: JSON.stringify(formInput),
                headers: {
                    'Content-Type': 'application/json',
                },
            })

            .then((response) => response.text())
            .then((noteStatus) => {
                document.querySelector(`#note-${formInput.note_id}`).remove()
                document.querySelector(`#edit-notes-${formInput.note_id}`).remove()
                document.querySelector(`#remove-notes-${formInput.note_id}`).remove()
            });
        });
    };
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