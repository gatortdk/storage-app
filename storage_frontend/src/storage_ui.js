import React, { useState, useEffect } from "react";

function StorageUnits() {
  const [units, setUnits] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/units/")
      .then((response) => response.json())
      .then((data) => setUnits(data))
      .catch((error) => console.error("Error fetching units:", error));
  }, []);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold text-center mb-6">Storage Units</h1>
      <div className="overflow-x-auto">
        <table className="table-auto w-full bg-white shadow-lg rounded-lg">
          <thead>
            <tr className="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
              <th className="py-3 px-6 text-left">Unit ID</th>
              <th className="py-3 px-6 text-left">Size</th>
              <th className="py-3 px-6 text-left">Price</th>
              <th className="py-3 px-6 text-left">Status</th>
              <th className="py-3 px-6 text-center">Actions</th>
            </tr>
          </thead>
          <tbody className="text-gray-600 text-sm font-light">
            {units.map((unit) => (
              <tr key={unit.unit_id} className="border-b border-gray-200 hover:bg-gray-100">
                <td className="py-3 px-6 text-left">{unit.unit_id}</td>
                <td className="py-3 px-6 text-left">{unit.size}</td>
                <td className="py-3 px-6 text-left">${unit.price}</td>
                <td className="py-3 px-6 text-left">
                  {unit.occupied ? "Occupied" : "Available"}
                </td>
                <td className="py-3 px-6 text-center">
                  <button className="text-blue-500 hover:underline mr-2">Edit</button>
                  <button className="text-red-500 hover:underline">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default StorageUnits;
