import React from "react";
import StorageUnits from "./storage_ui";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
          Storage Management System
        </h1>
        <StorageUnits />
      </div>
    </div>
  );
}

