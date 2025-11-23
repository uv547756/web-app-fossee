import axios from 'axios';
export const BASE_API = 'http://127.0.0.1:8000'
export const SAMPLE_CSV_PATH = '../backend/sample_equipment_data.csv'

export const api = axios.create({
    baseURL: BASE_API,
    timeout: 30000,
})

export async function uploadFile(file) {
    if (!file) {
        throw new Error("File not provided.")
    }
    

    const form = new FormData();
    form.append('file', file);

    const res = await api.post('/upload/', form, {
        headers: { 'Content-Type': 'multipart/form-data'},
    })
    return res.data;


}

export async function fetchHistory() {
    const res = await api.get('/history/');
    return res.data;
}

export function prepTypeChart(typeDistribution = {}) {
    const labels = Object.keys(typeDistribution);
    const data = labels.map((k) => typeDistribution[k]);

    return {
        labels,
        datasets: [
            {
                label: "Count by Type",
                data,
            }
        ]
    }
}

export function prepFlowrateChart(rows = []) {
  const labels = rows.map((r, i) => r['Equipment Name'] || r['Equipment'] || `Item ${i + 1}`);

  const data = rows.map((r) => {
    const v = r.Flowrate ?? r['Flowrate'] ?? r.flowrate ?? r['Flow Rate'] ?? 0;
    return Number(v) || 0;
  });

  return {
    labels,
    datasets: [
      {
        label: 'Flowrate',
        data,
        fill: false,

        borderWidth: 2,
        tension: 0.3,
      },
    ],
  };
}
