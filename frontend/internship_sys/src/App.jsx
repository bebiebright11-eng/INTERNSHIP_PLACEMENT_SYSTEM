import { useState } from 'react';
import axios from 'axios';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // This sends the data to your Django backend
      const response = await axios.post('http://127.0.0.1:8000/api/login/', {
        username: username,
        password: password
      });
      setMessage("Login Successful! Welcome, " + username);
    } catch (error) {
      setMessage("Login Failed. Check your backend settings.");
    }
  };

  return (
    <div style={{ padding: '40px', maxWidth: '400px', margin: 'auto', fontFamily: 'Arial' }}>
      <h2>Internship System Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:</label><br />
          <input 
            type="text" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            style={{ width: '100%', marginBottom: '10px' }}
          />
        </div>
        <div>
          <label>Password:</label><br />
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            style={{ width: '100%', marginBottom: '20px' }}
          />
        </div>
        <button type="submit" style={{ padding: '10px 20px', cursor: 'pointer' }}>
          Login
        </button>
      </form>
      {message && <p style={{ marginTop: '20px', color: 'blue' }}>{message}</p>}
    </div>
  );
}

export default App;