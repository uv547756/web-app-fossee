import React, { useEffect, useState } from 'react';
import Dashboard from './pages/Dashboard';
import Login from './Components/Login';
import { initAuth, setAuthToken } from './api';


// Chart.js registration (required)
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    initAuth(); // loads access token from localStorage
    const token = localStorage.getItem("accessToken");
    if (token) {
      setAuthToken(token);
      setAuthenticated(true);
    }
  }, []);

   const handleLoggedIn = (data) => {
    // This function is called from Login.js
    setAuthenticated(true);
  };

  return (
    <div style={{ background: '#f5f7fb', minHeight: '100vh', padding: 20 }}>
      {authenticated ? (
        <Dashboard />
      ) : (
        <Login onLoggedIn={handleLoggedIn} />
      )}
    </div>
  );
}

export default App;
