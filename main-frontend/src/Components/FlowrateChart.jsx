import { Line } from 'react-chartjs-2'
import { prepFlowrateChart } from '../api'
import { Legend, plugins, Tooltip } from 'chart.js';

export default function FlowrateChart({ rows }) {
    if (!rows|| rows.length === 0) {
    return (
      <div style={{ background: '#fff', padding: 12, borderRadius: 6 }}>
        <h4 style={{ marginTop: 0 }}>Flowrate (sample)</h4>
        <div style={{ color: '#666', padding: 12 }}>No row-sample available. Upload a CSV or enable rows_sample in the backend.</div>
      </div>
    );
  };
    const data = prepFlowrateChart(rows);
    const options = {
        responsive: true,
        plugins: {
            Legend: {display:true, position: 'top'},
            Tooltip: {mode: 'index', intersect: false},

        },
        scales: {
            x: {
                title: { display: true, text: 'Equipment'},
            },
            y: {
                title: { display: true, text: 'Flowrate' },
                beginAtZero: true,
            }
        }
    }
    return (
        <div style={{ background: '#fff', padding: 12, borderRadius: 6}}>
            <h4 style={{ marginTop: 0}}>Flowrate (sample)</h4>
            <Line data={data} />
        </div>
    );
}