const search = document.querySelector("#search");
const resultSection = document.querySelector("#result-section");

search.addEventListener("input", async function() {
    let response = await fetch('/search?q=' + search.value);
    let shows = await response.text();
    resultSection.classList.remove("hidden");
    if(!resultSection.classList.contains("hidden") && (shows.length < 20 || search.value == "")) {
        resultSection.classList.add("hidden");
    }
    document.querySelector('#search-result').innerHTML = shows;
});


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
    resultSection.classList.add("hidden");
});