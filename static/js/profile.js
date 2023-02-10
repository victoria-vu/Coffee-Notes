// Delete Recommendation from Profile Page


const removeRecommendationButton = document.querySelector('#remove-recc');

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
            window.location.reload();
         }, 4000);
    })
});

// Delete Review from Profile Page
const deleteReview = document.querySelector('#delete-review');

deleteReview.addEventListener('submit', (evt) => {
    evt.preventDefault();

    const formInput = {
        cafe_id: document.querySelector('#cafe-id').value
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
        document.querySelector('#customer-review').remove()
        document.querySelector('#remove-review-status').innerHTML = reviewStatus;
        setTimeout(function() {
            window.location.reload();
            }, 4000);
        });
    });