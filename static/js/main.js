const reviewSection = document.querySelector("#review-section");
document.querySelector("#write-review-btn").addEventListener("click", function() {
    reviewSection.classList.remove("hidden");
    reviewSection.classList.add("block");
});


document.querySelector("#close-review-btn").addEventListener("click", closeReviewSection);


function closeReviewSection() {
    reviewSection.classList.remove("block");
    reviewSection.classList.add("hidden");
}


/* review form on submission */
document.querySelector("#review-form").addEventListener("submit", function(e) {
    e.preventDefault();

    let request = new XMLHttpRequest();

    // response on load
    request.onload = () => {
        if (request.readyState == 4 && request.status == 200) {
            // DO NOT FORGET:
                // close the form
                // success message
            document.querySelector("#messages").innerHTML = request.responseText;
            
            closeReviewSection();
            /* if(response != "error") {
            //     closeReviewSection();
            } */
        }
    }

    const anime_id = document.querySelector("#anime-id").value;
    // request method
    request.open("POST", `../send_review/${anime_id}`, true);


    // fill the form with datas
    let review = new FormData();
    review.append("review", document.querySelector("#review").value);
    review.append("anime-id", document.querySelector("#anime-id").value);

    // send request
    request.send(review);
});