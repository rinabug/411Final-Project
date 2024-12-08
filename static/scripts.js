document.getElementById("recommend-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const genre = document.getElementById("genre").value;
    const rating = document.getElementById("rating").value;
    const recency = document.getElementById("recency").value;

    // Show the loading spinner
    document.getElementById("loading").style.display = "block";
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = ""; // Clear previous results

    try {
        const response = await fetch(`/api/recommend-movies?genre=${encodeURIComponent(genre)}&rating=${encodeURIComponent(rating)}&recency=${encodeURIComponent(recency)}`);
        const data = await response.json();

        resultsDiv.innerHTML = "<h2>Recommended Movies:</h2>";

        if (data.recommended_movies && data.recommended_movies.length > 0) {
            data.recommended_movies.forEach(movie => {
                const movieDiv = document.createElement("div");
                movieDiv.classList.add("movie-item");

                movieDiv.innerHTML = `
                    <strong>${movie.title}</strong> (${movie.year})<br>
                    Rating: ${movie.rating}<br>
                    Genre: ${movie.genre}<br>
                    <div class="media">
                        ${movie.trailer
                            ? `<iframe width="560" height="315" src="${movie.trailer}" frameborder="0" allowfullscreen></iframe>`
                            : ""}
                        ${movie.poster
                            ? `<img src="${movie.poster}" alt="${movie.title} Poster" style="max-width: 200px; margin-top: 10px;">`
                            : ""}
                    </div>
                    ${movie.watch_providers && movie.watch_providers.length > 0
                        ? `<p><strong>Available on:</strong> ${movie.watch_providers.join(', ')}</p>`
                        : `<p><strong>Streaming Availability:</strong> Not available</p>`}
                `;
                resultsDiv.appendChild(movieDiv);
            });
        } else {
            resultsDiv.innerHTML += "<p>No movies found. Try a different query.</p>";
        }
    } catch (error) {
        console.error("Error fetching recommendations:", error);
    } finally {
        // Hide the loading spinner after the data is loaded
        document.getElementById("loading").style.display = "none";
    }
});

// Fetch and display top-rated movies
document.getElementById("top-rated-btn").addEventListener("click", async function () {
    const resultsDiv = document.getElementById("additional-results");
    resultsDiv.innerHTML = ""; // Clear previous results

    try {
        const response = await fetch("/api/top-rated-movies");
        const data = await response.json();

        resultsDiv.innerHTML = "<h2>Top-Rated Movies:</h2>";
        if (data.top_rated_movies && data.top_rated_movies.length > 0) {
            data.top_rated_movies.forEach(movie => {
                const movieDiv = document.createElement("div");
                movieDiv.classList.add("movie-item");
                movieDiv.innerHTML = `
                    <strong>${movie.title}</strong> (${movie.release_date.split("-")[0]})<br>
                    Rating: ${movie.vote_average}<br>
                    ${movie.poster
                        ? `<img src="${movie.poster}" alt="${movie.title} Poster" style="max-width: 200px; margin-top: 10px;">`
                        : `<p>No poster available</p>`}
                `;
                resultsDiv.appendChild(movieDiv);
            });
        } else {
            resultsDiv.innerHTML += "<p>No movies found.</p>";
        }
    } catch (error) {
        console.error("Error fetching top-rated movies:", error);
    }
});

// Fetch and display now-playing movies
document.getElementById("now-playing-btn").addEventListener("click", async function () {
    const resultsDiv = document.getElementById("additional-results");
    resultsDiv.innerHTML = ""; // Clear previous results

    try {
        const response = await fetch("/api/now-playing");
        const data = await response.json();

        resultsDiv.innerHTML = "<h2>Now Playing Movies:</h2>";
        if (data.now_playing_movies && data.now_playing_movies.length > 0) {
            data.now_playing_movies.forEach(movie => {
                const movieDiv = document.createElement("div");
                movieDiv.classList.add("movie-item");
                movieDiv.innerHTML = `
                    <strong>${movie.title}</strong> (${movie.release_date.split("-")[0]})<br>
                    Rating: ${movie.vote_average}<br>
                    ${movie.poster
                        ? `<img src="${movie.poster}" alt="${movie.title} Poster" style="max-width: 200px; margin-top: 10px;">`
                        : `<p>No poster available</p>`}
                `;
                resultsDiv.appendChild(movieDiv);
            });
        } else {
            resultsDiv.innerHTML += "<p>No movies found.</p>";
        }
    } catch (error) {
        console.error("Error fetching now-playing movies:", error);
    }
});

// Search and display movies by title
document.getElementById("search-btn").addEventListener("click", async function () {
    const query = document.getElementById("search-query").value.trim();
    const resultsDiv = document.getElementById("additional-results");
    resultsDiv.innerHTML = ""; // Clear previous results

    if (!query) {
        resultsDiv.innerHTML = "<p>Please enter a movie title to search.</p>";
        return;
    }

    try {
        const response = await fetch(`/api/search-movies?query=${encodeURIComponent(query)}`);
        const data = await response.json();

        resultsDiv.innerHTML = `<h2>Search Results for "${query}":</h2>`;
        if (data.search_results && data.search_results.length > 0) {
            data.search_results.forEach(movie => {
                const movieDiv = document.createElement("div");
                movieDiv.classList.add("movie-item");
                movieDiv.innerHTML = `
                    <strong>${movie.title}</strong> (${movie.release_date ? movie.release_date.split("-")[0] : "Unknown"})<br>
                    Rating: ${movie.vote_average}<br>
                    ${movie.poster
                        ? `<img src="${movie.poster}" alt="${movie.title} Poster" style="max-width: 200px; margin-top: 10px;">`
                        : `<p>No poster available</p>`}
                `;
                resultsDiv.appendChild(movieDiv);
            });
        } else {
            resultsDiv.innerHTML += "<p>No movies found.</p>";
        }
    } catch (error) {
        console.error("Error searching for movies:", error);
    }
});
