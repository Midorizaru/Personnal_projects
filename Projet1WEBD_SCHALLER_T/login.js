function loginForm() {
    let options = {
        method: 'GET',
        headers: {
        accept: 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2OWRmYmRkNTBjZDQ5YzhjODk2OTliMWUxNGY0YTY1YiIsInN1YiI6IjY1YjIxZDdjYTgwMjM2MDE4NmFlYzlhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.IERYhDAVtn3F0x9NjUiFBY6k0hWY1v_zoOQT62vKepw'
        }
    };


    fetch(`https://api.themoviedb.org/3/authentication/token/new`, options)
        .then(response => response.json())
        .then(response => {
            let token = response.request_token;
            console.log(token);
            window.location.href = `https://www.themoviedb.org/authenticate/${token}?redirect_to=http://127.0.0.1:5500/index.html`;
            })
        .catch(err => console.error(err));


}

loginForm();