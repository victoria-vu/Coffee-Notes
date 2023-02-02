'use strict';

// Remove Bookmark on Bookmark Page
// Select the form ID
const unbookmarkButton = document.querySelector('#remove-bookmarkcafe');

// Create an event listener that handles when the "Remove Bookmark" is pressed
unbookmarkButton.addEventListener('submit', (evt) => {
    evt.preventDefault();

    // Selects the ID of the particular button and pulls the value from it, which is the cafe_id
    const formInput = {
        cafe_id: document.querySelector('#bookmarkcafe-id').value
    };

    fetch(`/cafe/${formInput.cafe_id}/removebookmark`, {
        method: 'POST',
        body: JSON.stringify(formInput),
        headers: {
            'Content-Type': 'application/json',
        },
    })

    .then((response) => response.text())
    .then((bookmarkStatus) => {
        document.querySelector('#bookmarkcafe-info').remove()
        document.querySelector('#remove-bookmark').remove()
        document.querySelector('#removebookmark-status').innerHTML = bookmarkStatus;
        setTimeout(function() {
            window.location.reload();
         }, 4000);
    });
})
