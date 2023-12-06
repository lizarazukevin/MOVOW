import React, { useState, useEffect } from 'react'
import Button from '../../components/Button'

function ShowsPage() {
  const [shows, setShows] = useState([]);

  useEffect(() => {
    getShows();
  }, [])

  const getShows = async () => {
    try {
      const response = await fetch('/api/shows/');
      const data = await response.json();
      setShows(data);
    } catch (error) {
      console.error('Error fetching shows: ', error);
    }
  };


  return (
    <div>
        <h1>Shows Page</h1>
        <Button to='/'>Home Page</Button>
        <br/>
        <p>Shows In Database: {shows.length}</p>
            <div className='shows-list'>
                {shows.map((show, index) => (
                    <div key={index} className='show-item'>
                        <p>Title: {show.show_title}, Release Date: {show.initial_release}, Episodes: {show.num_episodes}</p>
                    </div>
                ))}
            </div>
    </div>
    
  )
}

export default ShowsPage