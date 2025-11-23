import React, { useState } from 'react';
import { login } from '../api';

export default function Login({ onLoggedIn }) {
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setErr(null);
    setLoading(true);
    try {
      const data = await login(user, pass);
      onLoggedIn && onLoggedIn(data);
    } catch (e) {
      setErr('Login failed: ' + (e.response?.data?.detail || e.message));
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input placeholder="username" value={user} onChange={e => setUser(e.target.value)} />
      <input placeholder="password" type="password" value={pass} onChange={e => setPass(e.target.value)} />
      <button type="submit" disabled={loading}>{loading ? 'Logging in...' : 'Login'}</button>
      {err && <div style={{color:'crimson'}}>{err}</div>}
    </form>
  );
}

export function logout() {
  setAuthToken(null);
  localStorage.removeItem('refreshToken');
}
