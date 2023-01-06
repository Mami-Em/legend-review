

/*
  KITSU API:
    * base:
      -https://kitsu.io/api/edge
      -https://kitsu.io/api/edge/anime/id

    * search:
      -https://kistu.io/api/edge/anime?filter[text]=title '%20'

    * next page:
      -"links": {
        "first": "https://kitsu.io/api/edge/anime?page[limit]=5&page[offset]=0",
        "next": "https://kitsu.io/api/edge/anime?page[limit]=5&page[offset]=5"
      }

    * sort:
      -https://kitsu.io/api/edge/anime?sort=-startDate


    * include
      -https://kitsu.io/api/edge/anime/id?include=reviews

    * show only
      -https://kitsu.io/api/edge/anime/
*/


document.addEventListener("DOMContentLoaded", () => {

  // menu btn
  const menu = document.querySelector("#menu");
  const menuSection=document.querySelector("#menu-section");
  
  // show menu
  document.querySelector("#menu-btn").addEventListener("click", function() {
    menuSection.classList.remove("hidden");
    menu.classList.remove("hide-menu");
    setTimeout(() => {
      menu.classList.add("show-menu");
      menu.classList.remove("left-[-300px]");
    }, 50);
  });
  
  // hide menu
  document.querySelector("#hide-menu-btn").addEventListener("click", function() {
    menu.classList.remove("show-menu");
    menu.classList.add("hide-menu");
    menu.classList.add("left-[-300px]");
    setTimeout(() => {
      menuSection.classList.add("hidden");
    },200);
  
  });
  
  
  const searchBar = document.querySelector("#search-bar");
  const searchSection = document.querySelector("#search-section");
  
  // show search bar
  document.querySelector("#search-btn").addEventListener("click", function() {
    searchSection.classList.remove("hidden");
    searchBar.classList.remove("slide-sb");
    setTimeout(() => {
      searchBar.classList.remove("top-[-60px]");
      searchBar.classList.add("show-sb");
    }, 50);

    document.querySelector("#search").focus();
  });
  
  
  // close search bar
  document.querySelector("#close-search").addEventListener("click", function() {
    searchBar.classList.remove("show-sb"); 
    searchBar.classList.add("slide-sb");
    searchBar.classList.add("top-[-60px]");
    setTimeout(() => {
      searchSection.classList.add("hidden");
    }, 200);
  });

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


document.querySelector("#review-btn").addEventListener("click", () => {
  document.querySelector("#messages").classList.remove("hidden")
});