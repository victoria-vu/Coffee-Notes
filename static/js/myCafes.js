'use strict';

// Remove Cafe Visit on My Cafes Page
const removeVisitButton = document.querySelector('#remove-visitcafe');

removeVisitButton.addEventListener('submit', (evt) => {
    evt.preventDefault();

    // Selects the ID of the particular button and pulls the value from it, which is the cafe_id
    const formInput = {
        cafe_id: document.querySelector('#visitcafe-id').value
    };

    fetch(`/cafe/${formInput.cafe_id}/removecafevisit`, {
        method: 'POST',
        body: JSON.stringify(formInput),
        headers: {
            'Content-Type': 'application/json',
        },
    })

    .then((response) => response.text())
    .then((visitStatus) => {
        document.querySelector('#visitcafe-info').remove()
        document.querySelector('#my-cafe-notes').remove()
        document.querySelector('#cafe-note').remove()
        document.querySelector('#remove-visitcafe').remove()
        document.querySelector('#remove-visit-status').innerHTML = visitStatus;
        setTimeout(function() {
            window.location.reload();
         }, 4000);
    });
});


// Google Maps API
function initMap() {
    const map = new google.maps.Map(document.querySelector('#map'), {
        center: {
            lat: 37.601773,
            lng: -122.20287,
        },
        zoom: 11,
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