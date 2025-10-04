import React from 'react';
import ReactDOM from 'react-dom/client'; // Updated import for React 18
import './index.css'; // Ensure Tailwind CSS is imported
import App from './App'; // Adjust the path if necessary

const root = ReactDOM.createRoot(document.getElementById('root')); // Use createRoot API
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);