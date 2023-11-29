import React, { useState, useEffect } from 'react';

const HomePage = () => {
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        getMovies();
    }, []);

    const getMovies = async () => {
        try {
            const response = await fetch('/api/movies/');
            console.log(response)
            const data = await response.json();
            setMovies(data);
        } catch (error) {
            console.error('Error fetching movies:', error);
        }
    };

    return (
        <div className='home'>
            <h1>MOVOW Home</h1>
            <p>Movies In Database: {movies.length}</p>

            <div className='movies-list'>
                {movies.map((movie, index) => (
                    <div key={index} className='movie-item'>
                        <p>Title: {movie.movie_title}, Release Date: {movie.release_date}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default HomePage;
