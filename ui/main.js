

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
*/


// menu btn
const menu = document.querySelector("#menu");
const menuSection=document.querySelector("#menu-section");
document.querySelector("#menu-btn").addEventListener("click", function() {
  // show menu section
  menuSection.classList.remove("hidden");
  menu.classList.remove("close-menu");
  setTimeout(() => {
    menu.classList.add("show-menu");
  }, 300);

});

// close menu btn
document.querySelector("#close-menu-btn").addEventListener("click", function() {

  menu.classList.remove("show-menu");
  menu.classList.add("close-menu");

  setTimeout(() => {
    menuSection.classList.add("hidden");
  },200);

});