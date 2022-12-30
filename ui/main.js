

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
  
  // rm hide menu anim
  if (menu.classList.contains("hide-menu")) {
    menu.classList.remove("hide-menu");
  };

  // slide menu in after .05s
  setTimeout(() => {
    menu.classList.add("show-menu");
    menu.classList.remove("left-[-300px]");
  }, 50);
});

// hide menu btn
document.querySelector("#hide-menu-btn").addEventListener("click", function() {

  // rm show menu anim
  menu.classList.remove("show-menu");

  // slide out menu
  menu.classList.add("hide-menu");
  menu.classList.add("left-[-300px]");

  // rm blur bg after .2s
  setTimeout(() => {
    menuSection.classList.add("hidden");
  },200);

});