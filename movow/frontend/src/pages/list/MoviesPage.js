import React, { useState, useEffect } from 'react'
import Button from '../../components/Button'

const MoviesPage = () => {
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        getMovies();
    }, []);

    const getMovies = async () => {
        try {
            const response = await fetch('/api/movies/');
            const data = await response.json();
            setMovies(data);
        } catch (error) {
            console.error('Error fetching movies:', error);
        }
    };

    return (
        <div className='home'>
            <h1>Movies</h1>
            <Button to='/'>Movies Page</Button>
            <br/>
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

export default MoviesPage;