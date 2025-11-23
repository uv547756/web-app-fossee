import { useEffect, useState } from "react";
import { fetchHistory } from "../api";

export default function HistoryList({ onLoad }){
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let mounted = true;
        setLoading(true);
        fetchHistory()
            .then((data) => {
                if (mounted) setHistory(data);
            })
            .catch(() => {})
            .finally(() => mounted && setLoading(false));
        return () => (mounted = false);
    }, []);

    return (
        <div style={{ padding: 12, background: '#fff', borderRadius: 6}}>
            <h4 style={{ marginTop: 0 }}>History (last 5)</h4>
            {loading && <div>Loading...</div>}
            {!loading && history.length === 0 && <div>No uploads yet</div>}
            <ul style={{ listStyle: 'none', padding: 0, margin: 0}}>
                {history.map((h) => (
          <li key={h.id} style={{ borderBottom: '1px solid #eee', padding: '8px 0' }}>
            <div style={{ fontSize: 13, fontWeight: 600 }}>
              #{h.id} — {new Date(h.uploaded_at).toLocaleString()}
            </div>
            <div style={{ fontSize: 12, color: '#555' }}>
              Count: {h.total_count} — Avg Flow: {h.avg_flowrate}
            </div>
            <div style={{ marginTop: 6 }}>
              <button onClick={() => onLoad(h)} style={{ marginRight: 8, padding: '6px 8px' }}>
                Load
              </button>
              <a href={h.file} target="_blank" rel="noreferrer" style={{ fontSize: 12 }}>
                Download CSV
              </a>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
