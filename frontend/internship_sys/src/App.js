import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './studentlogin';
import StudentDashboard from './studentDashboard';


function App() {
  // Simple check to see if user is logged in
  const isAuthenticated = !!localStorage.getItem('token');

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      
      <Route 
        path="/dashboard" 
        element={isAuthenticated ? <StudentDashboard /> : <Navigate to="/login" />} 
      />

      {/* Redirect root to login or dashboard based on auth */}
      <Route 
        path="/" 
        element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} 
      />
    </Routes>
  );
}

export default App;