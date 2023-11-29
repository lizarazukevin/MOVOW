import {
  HashRouter as Router,
  Route,
  Routes
} from 'react-router-dom';
import HomePage from './pages/HomePage'
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' exact Component={HomePage}/>
      </Routes>
    </Router>
  );
}

export default App;
