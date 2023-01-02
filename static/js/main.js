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


// review stars

const stars = document.querySelectorAll(".review-stars");
let rated = 0;

stars.forEach(element => {
  element.addEventListener("click", () => {
    const selectedRate = element.dataset.rate;
    rated = selectedRate;
      stars.forEach(e => {
        const rate = e.dataset.rate;
        rate <= selectedRate ? e.classList.add('fill-zinc-900') : e.classList.remove('fill-zinc-900');
      });
  });
});


// show review
const reviewSection = document.querySelector("#review-section");
const reviewSh = document.querySelector("#review-sh");


document.querySelector("#review-btn").addEventListener("click", () => {
  reviewSection.classList.remove("hidden");
  reviewSh.classList.remove("hide-review-section");
  setTimeout(() => {
    reviewSh.classList.add("show-review-section");
    reviewSh.classList.remove("-bottom-[50rem]");
  }, 50);
});


document.querySelector("#close-review-section").addEventListener("click", closeReviewSection);

function closeReviewSection() {
  reviewSh.classList.remove("show-review-section");
  reviewSh.classList.add("hide-review-section");
  reviewSh.classList.add("-bottom-[50rem]");
  setTimeout(() => {
    reviewSection.classList.add("hidden");
  }, 200);
};