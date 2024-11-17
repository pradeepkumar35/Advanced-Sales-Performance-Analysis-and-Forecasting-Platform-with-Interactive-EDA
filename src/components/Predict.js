import React, { useState } from 'react';
import './Predict.css';

function Predict() {
  const [formData, setFormData] = useState({
    retailer: '',
    region: '',
    state: '',
    city: '',
    product: '',
    pricePerUnit: '',
    unitSold: '',
    costPerUnit: '',
  });

  const [profitData, setProfitData] = useState(null); // To store profit results and display after prediction

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handlePredict = () => {
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
  };

  return (
    <div className="predict">
      <h1>Profit Analysis</h1>
      {profitData ? (
        <div className="result">
          <h2>Profit Analysis Results</h2>
          <p>Profit Amount: ${profitData.profitAmount}</p>
          <p>Profit Percentage: {profitData.profitPercentage}%</p>
        </div>
      ) : (
        <div className="form-container">
          <div className="form-grid">
            <input type="text" name="retailer" placeholder="Retailer" onChange={handleChange} />
            <input type="text" name="region" placeholder="Region" onChange={handleChange} />
            <input type="text" name="state" placeholder="State" onChange={handleChange} />
            <input type="text" name="city" placeholder="City" onChange={handleChange} />
            <input type="text" name="product" placeholder="Product" onChange={handleChange} />
            <input type="number" name="pricePerUnit" placeholder="Price per Unit" onChange={handleChange} />
            <input type="number" name="unitSold" placeholder="Units Sold" onChange={handleChange} />
            <input type="number" name="costPerUnit" placeholder="Cost per Unit" onChange={handleChange} />
          </div>
          <button onClick={handlePredict}>Predict</button>
        </div>
      )}
    </div>
  );
}

export default Predict;
