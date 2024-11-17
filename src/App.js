import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Home from "./components/Home";
import UploadData from "./components/UploadData";
import Predict from "./components/Predict";
import Eda from "./components/Eda"; // Import EDA component
import TableauDashboard from "./components/TableauDashboard"; // Correct import for TableauDashboard
import "./index.css";

function App() {
  return (
    <Router>
      <div className="app">
        <Sidebar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/tableau" element={<TableauDashboard />} />
            <Route path="/upload" element={<UploadData />} />
            <Route path="/predict" element={<Predict />} />
            <Route path="/eda" element={<Eda />} /> {/* Add route for EDA */}
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
