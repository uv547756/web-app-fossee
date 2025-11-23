import axios from 'axios';
export const BASE_API = 'http://127.0.0.1:8000'
export const SAMPLE_CSV_PATH = '../backend/sample_equipment_data.csv'

export const api = axios.create({
    baseURL: BASE_API,
    timeout: 30000,
})

export function setAuthToken(accessToken) {
  if (accessToken) {
    api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
    localStorage.setItem('accessToken', accessToken);
  } else {
    delete api.defaults.headers.common['Authorization'];
    localStorage.removeItem('accessToken');
  }
}

export function initAuth() {
  const token = localStorage.getItem('accessToken');
  if (token) setAuthToken(token);
}

export async function login(username, password) {
  const res = await api.post('/api/token/', { username, password });
  const { access, refresh } = res.data;
  localStorage.setItem('refreshToken', refresh);
  setAuthToken(access);
  return res.data;
}

export async function refreshAccessToken() {
  const refresh = localStorage.getItem('refreshToken');
  if (!refresh) throw new Error('No refresh token');
  const res = await api.post('/api/token/refresh/', { refresh });
  const { access } = res.data;
  setAuthToken(access);
  return access;
}

let isRefreshing = false;
let failedQueue = [];

function processQueue(error, token = null) {
  failedQueue.forEach(prom => (error ? prom.reject(error) : prom.resolve(token)));
  failedQueue = [];
}

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const originalRequest = err.config;
    if (err.response && err.response.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise(function (resolve, reject) {
          failedQueue.push({ resolve, reject });
        }).then((token) => {
          originalRequest.headers['Authorization'] = 'Bearer ' + token;
          return api(originalRequest);
        }).catch(e => Promise.reject(e));
      }

      originalRequest._retry = true;
      isRefreshing = true;
      try {
        const newAccess = await refreshAccessToken();
        processQueue(null, newAccess);
        originalRequest.headers['Authorization'] = 'Bearer ' + newAccess;
        return api(originalRequest);
      } catch (e) {
        processQueue(e, null);
        setAuthToken(null);
        return Promise.reject(e);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(err);
  }
);

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

initAuth();