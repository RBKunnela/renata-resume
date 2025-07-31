const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files
app.use(express.static(__dirname));

// Serve the index.html file as the default
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Redirect any other routes to the main file
app.get('*', (req, res) => {
  res.redirect('/');
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});