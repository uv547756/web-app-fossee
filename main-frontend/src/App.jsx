import React from 'react';
import Dashboard from './pages/Dashboard';

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
  return (
    <div style={{ background: '#f5f7fb', minHeight: '100vh', padding: 20 }}>
      <Dashboard />
    </div>
  );
}

export default App;
