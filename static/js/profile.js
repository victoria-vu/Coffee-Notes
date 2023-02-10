// Delete Recommendation on My Cafes Page
const removeRecommendationButton = document.querySelector('#remove-recc');

removeRecommendationButton.addEventListener('submit', (evt) =>{
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
})