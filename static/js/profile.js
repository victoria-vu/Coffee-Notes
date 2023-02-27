'use strict';

// Edit User Information
const editInfoButton = document.querySelector('#edit-info-btn');
const userForm = document.querySelector('#edit-info');
const userRecc = document.querySelector('#edit-recommendation');

userForm.hidden = true;
userRecc.hidden = true;

editInfoButton.addEventListener('click', () => {
    if (userForm.hidden === true) {
        userForm.hidden = false;
        userRecc.hidden = false;
        editInfoButton.innerHTML = "Close Edit Profile";
        document.querySelector('#user-information').hidden = true;
    } else if (userForm.hidden === false) {
        userForm.hidden = true;
        userRecc.hidden = true;
        editInfoButton.innerHTML = "Edit Profile";
        document.querySelector('#user-information').hidden = false;
    }
});


// Remove Recommendation from Profile Page
const removeRecommendationButton = document.querySelector('#remove-recc');

if (removeRecommendationButton) {
    removeRecommendationButton.addEventListener('submit', (evt) => {
        evt.preventDefault();

        const formInput = {
            recommendation_id: document.querySelector('#remove-recc-id').value
        };

        fetch(`/profile/${formInput.recommendation_id}/removerecommendation`, {
            method: 'POST',
            body: JSON.stringify(formInput),
            headers: {
                'Content-Type': 'application/json',
            },    
        })

        .then((response) => response.text())
        .then((recommendationStatus) => {
            document.querySelector('#display-recc').remove()
            document.querySelector('#remove-recc-status').innerHTML = recommendationStatus;
            setTimeout(function() {
                document.querySelector('#remove-recc-status').innerHTML = '';
            }, 3000);
        });
    });
};


// Remove Review from Profile Page
const removeReviewButtons = document.querySelectorAll('.remove-review');

if (removeReviewButtons) {
    for (const button of removeReviewButtons) {
        button.addEventListener('submit', (evt) => {
            evt.preventDefault();

            const formInput = {
                cafe_id: button.id
            };

            fetch(`/profile/${formInput.cafe_id}/removereview`, {
                method: 'POST',
                body: JSON.stringify(formInput),
                headers: {
                    'Content-Type': 'application/json',
                },
            })

            .then((response) => response.text())
            .then((reviewStatus) => {
                document.querySelector(`#user-review-${formInput.cafe_id}`).remove()
                document.querySelector('#remove-review-status').innerHTML = reviewStatus;
                setTimeout(function() {
                    document.querySelector('#remove-review-status').innerHTML = '';
                }, 3000);
            });
        });
    }
};


// Edit Review on My Cafes Page
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
            // formID = edit-note-{{ review.review_id }}
            const formID = editButton.id.replace('btn', 'review');
            // Selects the correct form
            const form = document.querySelector(`#${formID}`)

                if (form.hidden === true) {
                    form.hidden = false;
                } else if (form.hidden === false) {
                        form.hidden = true;
                }
        });
    }
}