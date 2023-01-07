let value_rate = 0;

/* review form on submission */
document.querySelector("#review-form").addEventListener("submit", function(e) {
  e.preventDefault();

  let request = new XMLHttpRequest();
  
  // response on load
  request.onload = () => {
    if (request.readyState == 4 && request.status == 200) {
      
      document.querySelector("#messages-section").innerHTML = request.responseText;            
      closeReviewSection();
      
      const messages = document.querySelector("#messages");

      // send tht message
      document.querySelector("#messages-section").classList.remove("hidden");
      console.log(document.querySelector("#messages-section"));
      messages.classList.add("show-message");
      messages.classList.remove("close-message");
      setTimeout(() => {
        messages.classList.remove("-top-16");
      }, 100);
    }
  }

  const anime_id = document.querySelector("#anime-id").value;
  // request method
  request.open("POST", `../send_review/${anime_id}`, true);


  // fill the form with datas
  let review = new FormData();
  review.append("review", document.querySelector("#review").value);
  review.append("anime-id", document.querySelector("#anime-id").value);
  review.append("rate", value_rate);

  // send request
  request.send(review);
});



// review stars

const stars = document.querySelectorAll(".review-stars");

stars.forEach(element => {
  element.addEventListener("click", () => {
    const selectedRate = element.dataset.rate;
    value_rate = selectedRate;
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


// close message
function closeMessages() {
  messages.classList.remove("show-message");
  setTimeout(() => {
    messages.classList.add("close-message");
  }, 100);
  setTimeout(() => {
    messages.classList.add("-top-16");
    document.querySelector("#messages-section").classList.add("hidden");
  }, 300);
};