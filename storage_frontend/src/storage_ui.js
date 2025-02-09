import { createContext, useContext, useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";

// Create Context
const StorageContext = createContext();

export function StorageProvider({ children }) {
  const [units, setUnits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [editingUnit, setEditingUnit] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await axios.get("http://localhost:8000/units/");
        setUnits(response.data);
      } catch (err) {
        setError("Failed to fetch data.");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  return (
    <StorageContext.Provider value={{ units, loading, error, setUnits, editingUnit, setEditingUnit }}>
      {children}
    </StorageContext.Provider>
  );
}

export function useStorage() {
  return useContext(StorageContext);
}

export default function StorageUnits() {
  const { units, loading, error, setUnits, editingUnit, setEditingUnit } = useStorage();
  const { register, handleSubmit, reset, setValue } = useForm();

  const onSubmit = async (data) => {
    if (editingUnit) {
      // Update existing unit
      try {
        const response = await axios.put(`http://localhost:8000/units/${editingUnit.unit_id}`, data);
        setUnits((prevUnits) => prevUnits.map(unit => unit.unit_id === editingUnit.unit_id ? response.data : unit));
        setEditingUnit(null);
        reset();
      } catch (err) {
        console.error("Failed to update unit", err);
      }
    } else {
      // Add new unit
      try {
        const response = await axios.post("http://localhost:8000/units/", data);
        reset();
        setUnits((prevUnits) => [...prevUnits, response.data]);
      } catch (err) {
        console.error("Failed to save unit", err.response?.data?.detail || err.message);
      }
    }
  };

  const deleteUnit = async (unitId) => {
    try {
      await axios.delete(`http://localhost:8000/units/${unitId}`);
      setUnits((prevUnits) => prevUnits.filter(unit => unit.unit_id !== unitId));
    } catch (err) {
      console.error("Failed to delete unit", err);
    }
  };

  const startEditing = (unit) => {
    setEditingUnit(unit);
    setValue("unit_id", unit.unit_id);
    setValue("size", unit.size);
    setValue("price", unit.price);
    setValue("occupied", unit.occupied);
  };

  return (
    <div>
      <h2>Storage Units</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit(onSubmit)}>
        <input {...register("unit_id", { required: "Unit ID is required" })} placeholder="Unit ID" disabled={!!editingUnit} />
        <input {...register("size", { required: "Size is required" })} placeholder="Size" />
        <input {...register("price", { required: "Price is required", valueAsNumber: true })} placeholder="Price" type="number" />
        <label>
          <input {...register("occupied")} type="checkbox" /> Occupied
        </label>
        <button type="submit">{editingUnit ? "Update Unit" : "Add Unit"}</button>
      </form>

      {loading ? (
        <p>Loading storage units...</p>
      ) : (
        <table border="1" cellPadding="5" cellSpacing="0">
          <thead>
            <tr>
              <th>Unit ID</th>
              <th>Size</th>
              <th>Price</th>
              <th>Status</th>
              <th>Tenant</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {units.map((unit) => (
              <tr key={unit.unit_id}>
                <td>{unit.unit_id}</td>
                <td>{unit.size}</td>
                <td>${unit.price}</td>
                <td>{unit.occupied ? "Occupied" : "Available"}</td>
                <td>{unit.tenant ? unit.tenant.name : "N/A"}</td>
                <td>
                  <button onClick={() => startEditing(unit)}>Edit</button>
                  <button onClick={() => deleteUnit(unit.unit_id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

