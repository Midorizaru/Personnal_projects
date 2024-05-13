let page = 1
const btn = document.querySelector("#next_page")
      btn.style.display = 'block';
      btn.addEventListener('click', () => {
         page++; trendingMovies()})
      

function trendingMovies() {

    const options = {
        method: 'GET',
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2OWRmYmRkNTBjZDQ5YzhjODk2OTliMWUxNGY0YTY1YiIsInN1YiI6IjY1YjIxZDdjYTgwMjM2MDE4NmFlYzlhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.IERYhDAVtn3F0x9NjUiFBY6k0hWY1v_zoOQT62vKepw'
        }
      };
      
      fetch('https://api.themoviedb.org/3/trending/movie/day?language=fr-FR&page='+ page, options)
        .then(response => response.json())
        .then(response => {
            let divMovie = document.querySelector("#result");
            response.results.forEach(element => {
                newDiv = document.createElement("div");
                newDiv.className = "movie";
                newDiv.innerHTML = `
                
                  <img src = "https://image.tmdb.org/t/p/w200/${element.poster_path}">
                  <h1>${element.title}</h1>
                  <h4>${element.release_date}</h4>
                  <a href="movie.html?id=${element.id}">Voir plus</a>
                `;
                divMovie.appendChild(newDiv);
            });
            document.querySelectorAll('.view-more').forEach(link => {
              link.addEventListener('click', (event) => {
                  event.preventDefault();
                  const movieId = link.dataset.id;
                  movieDetails(movieId);
              });
          });
        })
        .catch(err => console.error(err))
          
}

trendingMovies()
