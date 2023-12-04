import React, { useState, useEffect } from 'react';

const HomePage = () => {
    const [movies, setMovies] = useState([]);
    const [shows, setShows] = useState([]);

    useEffect(() => {
        getMovies();
        getShows();
    }, []);

    const getMovies = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/movies/');
            console.log(response)
            const data = await response.json();
            setMovies(data);
        } catch (error) {
            console.error('Error fetching movies:', error);
        }
    };

    const getShows = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/shows/');
            console.log(response);
            const data = await response.json();
            setShows(data);
        } catch (error) {
            console.error('Error fetching shows: ', error);
        }
    }

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
            <p>Shows In Database: {shows.length}</p>
            <div className='show-list'>
                {shows.map((show, index) => (
                    <div key={index} className='show-item'>
                        <p>Title: {show.show_title}, Release Date: {show.initial_release}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default HomePage;
