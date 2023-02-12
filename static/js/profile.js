'use strict';

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