'use strict';

// Add Cafe to "My Cafes" Page from Cafe Details Page
// or Remove Cafe from "My Cafes" 
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
                window.location.reload();
            }, 2000);
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
                window.location.reload();
            }, 2000);
        });
    }}
);

// Delete Review from Cafe Details Page
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