document.querySelector("#write-review-btn").addEventListener("click", function() {
    const reviewSection = document.querySelector("#review-section");

    reviewSection.classList.remove("hidden");
    reviewSection.classList.add("block");
});