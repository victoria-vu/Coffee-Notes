'use strict';

// Bookmark a Cafe 
const bookmarkButton = document.querySelector('#bookmark-cafe');

bookmarkButton.addEventListener('submit', (evt) => {
    evt.preventDefault();
    // console.log('Form has been submitted.')

    const formInput = {
        cafe_id: document.querySelector('#cafe-id').value
    };

    fetch(`/cafe/${formInput.cafe_id}/bookmark`, {
        method: 'POST',
        body: JSON.stringify(formInput),
        headers: {
            'Content-Type': 'application/json',
        },
    })

        .then((response) => response.text())
        .then((bookmarkStatus) => {
            document.querySelector('#bookmark-button').innerHTML = 'Bookmarked';
            document.querySelector('#bookmark-status').innerHTML = bookmarkStatus;
            document.querySelector('#bookmark-button').disabled = true;
        })
});


//Changes HTML from "Bookmark This Cafe" to "Bookmarked"
// bookmarkButton.addEventListener('click', () => {
//     if (bookmarkButton.innerHTML === 'Bookmark This Cafe') {
//         bookmarkButton.innerHTML = 'Bookmarked';
//     } else if (bookmarkButton.innerHTML === 'Bookmarked') {
//         bookmarkButton.innerHTML = 'Bookmark This Cafe';
//     }
// });

// After hitting the button, grab the cafe_id
// Make a fetch request => method = "GET"
// Use the cafe_id number to create a url when hitting the button
// Will send information to the backend (server.py)
// Package flash message and send back to JS (jsonified)