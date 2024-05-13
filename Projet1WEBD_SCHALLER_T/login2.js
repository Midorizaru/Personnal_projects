function login2Form() {
    let options = {
        method: 'GET',
        headers: {
        accept: 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2OWRmYmRkNTBjZDQ5YzhjODk2OTliMWUxNGY0YTY1YiIsInN1YiI6IjY1YjIxZDdjYTgwMjM2MDE4NmFlYzlhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.IERYhDAVtn3F0x9NjUiFBY6k0hWY1v_zoOQT62vKepw'
        }
    };
    const url = window.location.search;
    const urlParameters = new URLSearchParams(url);
    token = urlParameters.get('request_token');

    let loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function (event) {
    event.preventDefault();

    let username = document.getElementById('Email').value;
    let password = document.getElementById('Password').value;

    let options = {
        method: 'POST',
        headers: {
            accept: 'application/json',
            'content-type': 'application/json',
            Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2OWRmYmRkNTBjZDQ5YzhjODk2OTliMWUxNGY0YTY1YiIsInN1YiI6IjY1YjIxZDdjYTgwMjM2MDE4NmFlYzlhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.IERYhDAVtn3F0x9NjUiFBY6k0hWY1v_zoOQT62vKepw'
        },
        body: JSON.stringify({
            username: username,
            password: password,
            request_token: token
        })
    };
    console.log(options);
    fetch(`https://api.themoviedb.org/3/authentication/token/validate_with_login`, options)
        .then(response => response.json())
        .then(response => {
            console.log(response);

        })

});
}

login2Form();