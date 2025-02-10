import React, { useState, useEffect } from "react";

function StorageUnits() {
    const [units, setUnits] = useState([]);
    const [newUnit, setNewUnit] = useState({ size: "", price: "", occupied: false });
    const [editingUnit, setEditingUnit] = useState(null); // Tracks the unit being edited

    useEffect(() => {
        fetchUnits();
    }, []);

    const fetchUnits = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/units/");
            if (!response.ok) throw new Error("Failed to fetch units");
            const data = await response.json();
            console.log("Fetched units:", data); // Log for debugging
            setUnits(data);
        } catch (error) {
            console.error("Error fetching units:", error);
        }
    };

    const handleAddUnit = async () => {
        try {
            const response = await fetch("http://127.0.0.1:8000/units/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(newUnit),
            });
            if (!response.ok) throw new Error("Failed to add unit");
            const data = await response.json();
            setUnits([...units, data]);
            setNewUnit({ size: "", price: "", occupied: false });
        } catch (error) {
            console.error("Error adding unit:", error);
        }
    };

    const handleSoftDeleteUnit = async (id) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/units/${id}`, {
                method: "DELETE",
            });
            if (!response.ok) throw new Error("Failed to delete unit");
            setUnits(units.filter((unit) => unit.unit_id !== id));
        } catch (error) {
            console.error("Error deleting unit:", error);
        }
    };

    const handleDeleteUnit = handleSoftDeleteUnit; // Ensure this is assigned after definition

    const handleEditUnit = (unit) => {
        setEditingUnit({ ...unit });
    };

    const handleSaveEdit = async () => {
        if (!editingUnit || !editingUnit.unit_id) return; // Prevent error on uninitialized unit_id

        try {
            const response = await fetch(`http://127.0.0.1:8000/units/${editingUnit.unit_id}/`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(editingUnit),
            });
            if (!response.ok) throw new Error("Failed to update unit");
            const updatedUnit = await response.json();
            setUnits(units.map((unit) => (unit.unit_id === updatedUnit.unit_id ? updatedUnit : unit)));
            setEditingUnit(null); // Exit editing mode
        } catch (error) {
            console.error("Error updating unit:", error);
        }
    };

    const handleCancelEdit = () => {
        setEditingUnit(null); // Exit editing mode without saving
    };

    return (
        <div className="p-6 bg-gray-50 min-h-screen">
          <h1 className="text-3xl font-bold text-center mb-6">Storage Management System</h1>
          <h2 className="text-2xl font-semibold text-center mb-6">Storage Units</h2>
          <div className="mb-4">
            <input
              type="text"
              placeholder="Size"
              value={newUnit.size}
              onChange={(e) => setNewUnit({ ...newUnit, size: e.target.value })}
              className="border rounded p-2 mr-2"
            />
            <input
              type="text"
              placeholder="Price"
              value={newUnit.price}
              onChange={(e) => setNewUnit({ ...newUnit, price: e.target.value })}
              className="border rounded p-2 mr-2"
            />
            <label className="mr-2">
              <input
                type="checkbox"
                checked={newUnit.occupied}
                onChange={(e) => setNewUnit({ ...newUnit, occupied: e.target.checked })}
                className="mr-1"
              />
              Occupied
            </label>
            <button
              onClick={handleAddUnit}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Add Unit
            </button>
          </div>
          <div className="overflow-x-auto">
            {units.length > 0 ? (
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
                      <td className="py-3 px-6 text-left">
                        {editingUnit && editingUnit.unit_id === unit.unit_id ? (
                          <input
                            type="text"
                            value={editingUnit.size}
                            onChange={(e) => setEditingUnit({ ...editingUnit, size: e.target.value })}
                            className="border rounded p-1"
                          />
                        ) : (
                          unit.size
                        )}
                      </td>
                      <td className="py-3 px-6 text-left">
                        {editingUnit && editingUnit.unit_id === unit.unit_id ? (
                          <input
                            type="number"
                            value={editingUnit.price}
                            onChange={(e) => setEditingUnit({ ...editingUnit, price: e.target.value })}
                            className="border rounded p-1"
                          />
                        ) : (
                          `$${unit.price}`
                        )}
                      </td>
                      <td className="py-3 px-6 text-left">
                        {unit.occupied ? "Occupied" : "Available"}
                      </td>
                      <td className="py-3 px-6 text-center">
                        {editingUnit && editingUnit.unit_id === unit.unit_id ? (
                          <>
                            <button onClick={handleSaveEdit} className="text-green-500 hover:underline mr-2">Save</button>
                            <button onClick={handleCancelEdit} className="text-gray-500 hover:underline">Cancel</button>
                          </>
                        ) : (
                          <>
                            <button onClick={() => handleEditUnit(unit)} className="text-blue-500 hover:underline mr-2">Edit</button>
                            <button onClick={() => handleDeleteUnit(unit.unit_id)} className="text-red-500 hover:underline">Delete</button>
                          </>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="text-center text-gray-600">No units available. Please add one.</p>
            )}
          </div>
        </div>
      );
    }

export default StorageUnits;

