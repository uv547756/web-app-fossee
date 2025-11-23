import { useState } from "react";
import { uploadFile, SAMPLE_CSV_PATH } from "../api";

export default function UploadForm({ onUploaded }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState(null);

    async function handleSubmit(e) {
        e.preventDefault();
        setErr(null);
        if (!file) return setErr('Choose a CSV first');
        try {
            setLoading(true);
            const dataset = await uploadFile(file);
            onUploaded(dataset);

        } catch (e) {
            console.log(e);
        } finally {
            setLoading(false);
            setFile(null);

            if (e.target && e.target.reset) e.target.reset();
        }
    }

    return (
        <div style={{ padding: 12, background: '#fff', borderRadius: 6, marginBottom: 12 }}>
          <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <input
              type="file"
              accept=".csv"
              onChange={(e) => setFile(e.target.files && e.target.files[0])}
            />
            <button type="submit" disabled={loading} style={{ padding: '8px 12px' }}>
              {loading ? 'Uploading...' : 'Upload CSV'}
            </button>
            <a href={SAMPLE_CSV_PATH} target="_blank" rel="noreferrer" style={{ marginLeft: 8 }}>
              Use sample CSV
            </a>
          </form>
          {err && <div style={{ color: 'crimson', marginTop: 8 }}>{err}</div>}
          <div style={{ marginTop: 8, fontSize: 12, color: '#666' }}>
            Endpoint: <code>/upload/</code> (form-data key = <code>file</code>)
          </div>
        </div>
      );
}