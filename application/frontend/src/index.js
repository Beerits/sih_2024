import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
// import './index.css'; // Import any global CSS here

// Create a root element and render the App component into it
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
