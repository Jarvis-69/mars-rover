// filepath: c:\Users\joris\mars-rover\backend\server.js
const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = process.env.PORT || 5000;

// Configuration de la connexion à la base de données
const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
});

// Gérer les requêtes CORS (Cross-Origin Resource Sharing)
// Permet aux frontends spécifiés d'appeler l'API
const allowedOrigins = ['http://localhost:3000', 'http://localhost:5000'];
app.use((req, res, next) => {
  const origin = req.headers.origin;
  if (allowedOrigins.includes(origin)) {
    res.header('Access-Control-Allow-Origin', origin); // Autorise l'origine spécifique si elle est dans la liste
  }
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});


// Middleware simple pour logguer les requêtes
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});

// Route simple pour vérifier la connexion BDD
app.get('/api/db-check', async (req, res) => {
  // Le header Access-Control-Allow-Origin est maintenant géré par le middleware global
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT NOW()'); // Simple requête
    client.release();
    res.json({ success: true, time: result.rows[0].now });
  } catch (err) {
    console.error('Database connection error', err.stack);
    // Le header Access-Control-Allow-Origin est maintenant géré par le middleware global
    res.status(500).json({ success: false, error: 'Database connection failed' });
  }
});

// Route de santé simple
app.get('/api/health', (req, res) => {
  res.json({ status: 'UP' });
});


app.listen(port, () => {
  console.log(`Backend server listening on port ${port}`);
});