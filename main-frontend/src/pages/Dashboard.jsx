import React, { useState } from 'react';
import UploadForm from '../Components/UploadForm';
import HistoryList from '../Components/HistoryList';
import SummaryCards from '../Components/SummaryCards';
import TypePieChart from '../Components/TypePieChart';
import FlowrateChart from '../Components/FlowrateChart';
import ReportButton from '../Components/ReportDownloader';

export default function Dashboard() {
  const [summary, setSummary] = useState(null);

  function handleUploaded(dataset) {
    setSummary(dataset);
  }

  function handleLoadFromHistory(dataset) {
    setSummary(dataset);
  }

  const fallbackFilePath = '/uploads/sample_equipment_data_X3d5OqH.csv';

  return (
    <div style={{ maxWidth: 1100, margin: '20px auto', padding: 12 }}>
      <h1 style={{ marginBottom: 12 }}>Chemical Equipment Visualizer — Dashboard</h1>

      <UploadForm onUploaded={handleUploaded} />

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 12 }}>
        <div>
          <div style={{ marginBottom: 12 }}>
            <SummaryCards summary={summary} />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <TypePieChart typeDistribution={summary ? summary.type_distribution : null} />
            <FlowrateChart rows={summary ? summary.rows : null} />
          </div>

          <div style={{ marginTop: 12 }}>
            <h4>Full summary JSON</h4>
            <pre style={{ background: '#e9e2e2ff', padding: 12, borderRadius: 6, maxHeight: 300, overflow: 'auto' }}>
              {summary ? JSON.stringify(summary, null, 2) : 'No summary loaded.'}
            </pre>
          </div>
        </div>

        <aside>
          {/* Report button: prefer datasetId when available, otherwise use fallback local path */}
          <div style={{ marginBottom: 12 }}>
            <ReportButton
              datasetId={summary ? summary.id : null}
              fileLocalPath={fallbackFilePath}
              baseApi="http://127.0.0.1:8000"
            />
          </div>
          <HistoryList onLoad={handleLoadFromHistory} />
        </aside>
      </div>
    </div>
  );
}
