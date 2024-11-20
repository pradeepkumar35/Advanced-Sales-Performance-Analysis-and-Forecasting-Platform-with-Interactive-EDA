import React, { useState } from "react";
import Papa from "papaparse"; // Import PapaParse for CSV handling
import "./Predict.css";

function Predict() {
  const [formData, setFormData] = useState({
    retailer: "",
    region: "",
    state: "",
    city: "",
    product: "",
    pricePerUnit: "",
    unitSold: "",
    costPerUnit: "",
  });

  const [csvData, setCsvData] = useState([]); // To store the entered data
  const [profitData, setProfitData] = useState(null); // To store profit results

  // Handle form data changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Handle profit calculation and adding data to csvData
  const handleAdd = () => {
    const { pricePerUnit, unitSold, costPerUnit } = formData;

    // Parse inputs to ensure numerical calculations
    const price = parseFloat(pricePerUnit) || 0;
    const units = parseInt(unitSold) || 0;
    const cost = parseFloat(costPerUnit) || 0;

    // Calculate total sales and total cost
    const totalSales = price * units;
    const totalCost = cost * units;

    // Calculate profit amount and profit percentage
    const profitAmount = totalSales - totalCost;
    const profitPercentage = totalCost ? (profitAmount / totalCost) * 100 : 0;

    // Store profit values to display after prediction
    setProfitData({
      profitAmount: profitAmount.toFixed(2),
      profitPercentage: profitPercentage.toFixed(2),
    });

    // Append the current form data and profit results to csvData
    const newEntry = {
      ...formData,
      profitAmount: profitAmount.toFixed(2),
      profitPercentage: profitPercentage.toFixed(2),
    };

    // Add new entry to the CSV data state
    setCsvData([...csvData, newEntry]);

    // Reset form for next entry
    setFormData({
      retailer: "",
      region: "",
      state: "",
      city: "",
      product: "",
      pricePerUnit: "",
      unitSold: "",
      costPerUnit: "",
    });
  };

  // Handle CSV download
  const handleDownload = () => {
    const csv = Papa.unparse(csvData); // Convert csvData to CSV format
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });

    // Create a download link and trigger a click to download the file
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "profit_data.csv"; // Set the filename
    link.click();
  };

  return (
    <div className="predict">
      <h1>Profit Analysis</h1>
      {profitData && (
        <div className="result">
          <h2>Profit Analysis Results</h2>
          <p>Profit Amount: ${profitData.profitAmount}</p>
          <p>Profit Percentage: {profitData.profitPercentage}%</p>
        </div>
      )}
      <div className="form-container">
        <div className="form-grid">
          <input
            type="text"
            name="retailer"
            value={formData.retailer}
            placeholder="Retailer"
            onChange={handleChange}
          />
          <input
            type="text"
            name="region"
            value={formData.region}
            placeholder="Region"
            onChange={handleChange}
          />
          <input
            type="text"
            name="state"
            value={formData.state}
            placeholder="State"
            onChange={handleChange}
          />
          <input
            type="text"
            name="city"
            value={formData.city}
            placeholder="City"
            onChange={handleChange}
          />
          <input
            type="text"
            name="product"
            value={formData.product}
            placeholder="Product"
            onChange={handleChange}
          />
          <input
            type="number"
            name="pricePerUnit"
            value={formData.pricePerUnit}
            placeholder="Price per Unit"
            onChange={handleChange}
          />
          <input
            type="number"
            name="unitSold"
            value={formData.unitSold}
            placeholder="Units Sold"
            onChange={handleChange}
          />
          <input
            type="number"
            name="costPerUnit"
            value={formData.costPerUnit}
            placeholder="Cost per Unit"
            onChange={handleChange}
          />
        </div>
        <button onClick={handleAdd}>Add</button>
      </div>

      {csvData.length > 0 && (
        <div className="download-container">
          <button onClick={handleDownload}>Download CSV</button>
        </div>
      )}
    </div>
  );
}

export default Predict;
