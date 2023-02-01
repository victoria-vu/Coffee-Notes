'use strict';

// Bookmark and Remove Bookmark on Cafe Page
const bookmarkSubmitButton = document.querySelector('#bookmark-cafe');

bookmarkSubmitButton.addEventListener('submit', (evt) => {
    evt.preventDefault();

    const bookmarkButton = document.querySelector('#bookmark-button');
    if (bookmarkButton.innerHTML === 'Bookmark This Cafe') {
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
                document.querySelector('#bookmark-button').innerHTML = 'Remove Bookmark';
                document.querySelector('#bookmark-status').innerHTML = bookmarkStatus;
                document.querySelector('#bookmark-button').disabled = true;
                setTimeout(function() {
                    window.location.reload();
                    }, 2000);
            })

     } else if (bookmarkButton.innerHTML === 'Remove Bookmark') {
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
            document.querySelector('#bookmark-button').innerHTML = 'Bookmark This Cafe';
            document.querySelector('#bookmark-status').innerHTML = bookmarkStatus;
            document.querySelector('#bookmark-button').disabled = true;
            setTimeout(function() {
                window.location.reload();
                }, 2000);
        });
    }
});