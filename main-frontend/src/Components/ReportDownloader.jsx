// src/components/ReportButton.js
import React, { useState } from 'react';
import axios from 'axios';

/**
 * ReportButton
 * Minimal component that shows two buttons:
 *  - "Open PDF" (opens URL in new tab)
 *  - "Download PDF" (downloads using axios blob; useful when auth is needed)
 *
 * Props:
 *  - datasetId (number | null) : if provided, component will open `{baseApi}/datasets/{datasetId}/report.pdf`
 *  - fileLocalPath (string) : fallback local path (your tool will map this to a URL). Default set from your upload history.
 *  - baseApi (string) : base host for dataset endpoint (default http://127.0.0.1:8000)
 *  - authToken (string|null) : optional 'Bearer <token>' if your endpoint is protected
 *
 * Usage examples:
 *  <ReportButton datasetId={26} />
 *  <ReportButton fileLocalPath="/uploads/sample_equipment_data_X3d5OqH.csv" />
 */
export default function ReportButton({
  datasetId = null,
  fileLocalPath = '/uploads/sample_equipment_data_X3d5OqH.csv', // fallback
  baseApi = 'http://127.0.0.1:8000',
  authToken = null,
}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Prefer dataset endpoint when datasetId provided; otherwise use fileLocalPath
  const reportUrl = datasetId ? `${baseApi}/datasets/${datasetId}/report.pdf` : fileLocalPath;

  function handleOpen() {
    setError(null);
    try {
      window.open(reportUrl, '_blank', 'noopener,noreferrer');
    } catch (e) {
      setError('Unable to open report in new tab.');
    }
  }

  async function handleDownload() {
    setError(null);
    setLoading(true);
    try {
      const config = {
        responseType: 'blob',
        headers: {},
      };
      if (authToken) config.headers['Authorization'] = authToken;

      const res = await axios.get(reportUrl, config);

      let filename = datasetId ? `dataset_${datasetId}_report.pdf` : 'report.pdf';
      const disp = res.headers['content-disposition'];
      if (disp) {
        const m = /filename\*=UTF-8''([^;]+)|filename="([^"]+)"|filename=([^;]+)/i.exec(disp);
        if (m) filename = decodeURIComponent(m[1] || m[2] || m[3]);
      }

      const blob = new Blob([res.data], { type: res.data.type || 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Report download failed', err);
      
      setError('Download failed — check server route, CORS, or auth.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      display: 'inline-flex',
      gap: 8,
      alignItems: 'center',
      background: '#fff',
      padding: 8,
      borderRadius: 6,
      boxShadow: '0 1px 0 rgba(0,0,0,0.04)'
    }}>
      <button onClick={handleOpen} style={{ padding: '6px 10px' }}>
        Open PDF
      </button>

      <button onClick={handleDownload} disabled={loading} style={{ padding: '6px 10px' }}>
        {loading ? 'Downloading…' : 'Download PDF'}
      </button>

      <div style={{ marginLeft: 8, fontSize: 12, color: '#666' }}>
        <div style={{ maxWidth: 320, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {reportUrl}
        </div>
        {error && <div style={{ color: 'crimson', marginTop: 6 }}>{error}</div>}
      </div>
    </div>
  );
}