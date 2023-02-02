'use strict';

// Add a Cafe to "My Cafes" Page from Cafe Details Page
// or Remove Cafe from "My Cafes"
const myCafeSubmitButton = document.querySelector('#cafe-visit');

myCafeSubmitButton.addEventListener('submit', (evt) => {
    evt.preventDefault();

    const myCafeButton = document.querySelector('#visit-button');
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
                document.querySelector('#visit-button').innerHTML = 'Remove from My Cafes';
                document.querySelector('#cafe-visit-status').innerHTML = myCafeStatus;
                document.querySelector('#visit-button').disabled = true;
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
                document.querySelector('#visit-button').innerHTML = 'Add to My Cafes';
                document.querySelector('#cafe-visit-status').innerHTML = myCafeStatus;
                document.querySelector('#visit-button').disabled = true;
                setTimeout(function() {
                    window.location.reload();
                }, 2000);
        });
    }
});
