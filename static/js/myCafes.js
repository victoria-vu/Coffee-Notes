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
})