
import React from "react";
import ReactDOM from "react-dom/client"; // Ensure correct import for React 18+
import App from "./App";
import { StorageProvider } from "./storage_ui"; // Import StorageProvider

// Render the app inside the StorageProvider context
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <StorageProvider>
      <App />
    </StorageProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
