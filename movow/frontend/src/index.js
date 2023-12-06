import React from 'react';
import ReactDOM from 'react-dom/client';
import reportWebVitals from './reportWebVitals';
import './index.css'

import HomePage from './pages/list/HomePage';
import MoviesPage from './pages/list/MoviesPage';
import ShowsPage from './pages/list/ShowsPage';
import ActorsPage from './pages/list/ActorsPage';
import ListsPage from './pages/list/ListsPage';
import ProfilesPage from './pages/list/ProfilesPage';
import SearchPage from './pages/list/SearchPage';

import MoviePage from './pages/detailed/MoviePage';
import ProfilePage from './pages/detailed/ProfilePage';
import ShowPage from './pages/detailed/ShowPage';
import ListPage from './pages/detailed/ListPage';

import {
  createBrowserRouter,
  RouterProvider
} from 'react-router-dom'

const router = createBrowserRouter([
  { path: '/', element: <HomePage/> },
  { path: '/movies', element: <MoviesPage/> },
  { path: '/shows', element: <ShowsPage/> },
  { path: '/lists', element: <ListsPage/> },
  { path: '/profiles', element: <ProfilesPage/> },
  { path: '/actors', element: <ActorsPage/> },
  { path: '/search', element: <SearchPage/> },
  { path: '/movies/:id', element: <MoviePage/> },
  { path: '/profiles/:id', element: <ProfilePage/> },
  { path: '/shows/:id', element: <ShowPage/> },
  { path: '/lists/:id', element: <ListPage/> }
])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>

    <RouterProvider router={router} />

  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
