// filepath: c:\Users\joris\mars-rover\frontend\src\App.js
import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [apiStatus, setApiStatus] = useState('Checking...');
  const [dbStatus, setDbStatus] = useState('Checking...');
  const apiUrl = process.env.REACT_APP_API_URL; // Récupère l'URL de l'API depuis les env vars

  useEffect(() => {
    // Vérifier la santé de l'API
    fetch(`${apiUrl}/api/health`)
      .then(res => res.ok ? res.json() : Promise.reject(`API Error: ${res.status}`))
      .then(data => setApiStatus(data.status || 'OK'))
      .catch(error => {
        console.error("API Health Check Failed:", error);
        setApiStatus('Error');
      });

    // Vérifier la connexion à la BDD via l'API
    fetch(`${apiUrl}/api/db-check`)
      .then(res => res.ok ? res.json() : Promise.reject(`DB Check Error: ${res.status}`))
      .then(data => setDbStatus(data.success ? `Connected (Server time: ${data.time})` : 'Connection Failed'))
      .catch(error => {
         console.error("DB Check Failed:", error);
         setDbStatus('Error');
      });
  }, [apiUrl]); // Dépendance à apiUrl pour re-fetch si elle change (peu probable ici)

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1>React App with Docker Compose</h1>
        <p>API URL: {apiUrl || 'Not Set'}</p>
        <p>Backend API Status: {apiStatus}</p>
        <p>Database Connection Status: {dbStatus}</p>
      </header>
    </div>
  );
}

export default App;