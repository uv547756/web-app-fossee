import { Pie } from 'react-chartjs-2';
import { prepTypeChart } from '../api';

export default function TypePieChart({typeDistribution}) {
    if (!typeDistribution) return null;

    const data = prepTypeChart(typeDistribution);
    const colors = data.labels.map((_, i) => `hsl(${(i * 55) % 360} 70% 50%)`);
    const chartData = { 
        ...data,
        datasets: data.datasets.map(ds => ({ ...ds, backgroundColor: colors })),
    };
    return (
        <div style={{ background: '#fff', padding: 12, borderRadius: 6 }}>
            <h4 style={{ marginTop: 0}}>Type Distribution</h4>
            <Pie data={chartData} />
        </div>
    );
}