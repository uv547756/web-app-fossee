function Card({ title, value, suffix }) {
  return (
    <div style={{
      padding: 12, borderRadius: 6, background: '#fff', boxShadow: '0 0 0 1px #eee inset'
    }}>
      <div style={{ fontSize: 12, color: '#666' }}>{title}</div>
      <div style={{ fontSize: 18, fontWeight: 700 }}>{value}{suffix ? ` ${suffix}` : ''}</div>
    </div>
  );
}

export default function SummaryCards({ summary }) {
  if (!summary) return null;
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
      <Card title="Total" value={summary.total_count} />
      <Card title="Avg Flowrate" value={summary.avg_flowrate} suffix="units" />
      <Card title="Avg Pressure" value={summary.avg_pressure} suffix="bar" />
      <Card title="Avg Temp" value={summary.avg_temperature} suffix="°C" />
    </div>
  );
}
