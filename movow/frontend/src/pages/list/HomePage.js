import React from 'react'

import Button from '../../components/Button'

const HomePage = () => {

    return (
        <div className='home'>
            <h1>MOVOW Home</h1>
            <h3>Generic List Pages</h3>
            <Button to='/'>Home Page</Button>
            <Button to='/movies'>Movies Page</Button>
            <Button to='/shows'>Shows Page</Button>
            <Button to='/lists'>Lists Page</Button>
            <Button to='/profiles'>Profiles Page</Button>
            <Button to='/actors'>Actors Page</Button>
            <Button to='/search'>Search Page</Button>
            <h4>Detailed Pages</h4>
            <Button to='/movies/0'>Sample Movie</Button>
            <Button to='/profiles/0'>Sample Profile</Button>
            <Button to='/shows/0'>Sample Show</Button>
            <Button to='/lists/0'>Sample List</Button>
        </div>
    );
};

export default HomePage;