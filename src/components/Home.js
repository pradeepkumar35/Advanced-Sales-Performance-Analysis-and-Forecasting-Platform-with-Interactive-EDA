import React from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

function Home() {
  const navigate = useNavigate();

  const redirectToTableau = () => {
    navigate("/tableau");
  };

  const handleEDA = () => {
    window.open(
      "https://pradeepkumar35-advanced-sales-performance-analysi-srcapp-k9vgz6.streamlit.app/",
      "_self"
    );
  };

  const handleForecast = () => {
    window.open(
      "https://pradeepkumar35-advanced-sales-perfo-srcsales-forecasting-n18vd8.streamlit.app/",
      "_self"
    );
  };

  return (
    <div className="home">
      <h1>Sales EDA Analysis and Forecast</h1>
      <div className="cards">
        <div
          className="card"
          onClick={handleEDA}
          style={{ cursor: "pointer" }}
          aria-label="Exploratory Data Analysis Card"
        >
          <h2>Exploratory Data Analysis</h2>
          <p>Data visualization</p>
        </div>
        <div
          className="card"
          onClick={handleForecast}
          style={{ cursor: "pointer" }}
          aria-label="Sales Forecasting Card"
        >
          <h2>Forecast Future Sales</h2>
          <p>Sales revenue in the future</p>
        </div>
        <div
          className="card"
          onClick={redirectToTableau}
          style={{ cursor: "pointer" }}
          aria-label="Tableau Dashboard Card"
        >
          <h2>Tableau Dashboard</h2>
          <p>View interactive dashboard</p>
        </div>
      </div>
    </div>
  );
}

export default Home;
