function movieDetails() {
    const options = {
        method: 'GET',
        headers: {
        accept: 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2OWRmYmRkNTBjZDQ5YzhjODk2OTliMWUxNGY0YTY1YiIsInN1YiI6IjY1YjIxZDdjYTgwMjM2MDE4NmFlYzlhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.IERYhDAVtn3F0x9NjUiFBY6k0hWY1v_zoOQT62vKepw'
        }
    };
    const url = window.location.search;
    const urlParameters = new URLSearchParams(url);
    movieId = urlParameters.get('id');


    fetch(`https://api.themoviedb.org/3/movie/${movieId}?language=fr-FR`, options)
    .then(response => response.json())
        .then(response => {
            let divDetail = document.querySelector("#detail");
            let newDiv = document.createElement("div");
            newDiv.className = "movie";
            newDiv.innerHTML = `
                <img src="https://image.tmdb.org/t/p/w200/${response.poster_path}">
                <h1>${response.title}</h1>
                <h4>${response.release_date}</h4>
                <p>${response.overview}</p>
            `;
            divDetail.appendChild(newDiv);
            })
            fetch(`https://api.themoviedb.org/3/movie/${movieId}/reviews`, options)
            .then(response => response.json())
            .then(overview => {
                for (let i = 0; i < overview.results.length; i++) {
                    let divComments = document.querySelector("#reviews");
                    let commentDiv = document.createElement("div");
                    commentDiv.className = "comment";
                    let avatarPath = overview.results[i].author_details.avatar_path;
                    let avatar;
                    if (avatarPath === null) {
                        avatar = "https://www.logiquetechno.com/wp-content/uploads/2020/11/retirer-photo-de-profil-facebook.png";
                    } else {
                        if (avatarPath.startsWith('/')) {
                            avatar = `https://image.tmdb.org/t/p/w200${avatarPath}`;
                        } else {
                            avatar = avatarPath;
                        }
                    }
                    commentDiv.innerHTML = `
                        <h3>${overview.results[i].author}</h3>
                        <img src="${avatar}" alt="Avatar" style="width: 60px; height: 40px;"></img>
                        <p>${overview.results[i].content}</p>
                        `;
                    divComments.appendChild(commentDiv);
                }
            })      
                    .catch(err => console.error(err));

}

movieDetails()
