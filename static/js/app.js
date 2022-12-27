const search = document.querySelector("#search");

search.addEventListener("input", async function() {
    let response = await fetch('/search?q=' + search.value);
    let shows = await response.text();
    document.querySelector('#search-result').innerHTML = shows;
});