import React from "react";

function EDA() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Exploratory Data Analysis</h1>
      <iframe
        src="https://pradeepkumar35-advanced-sales-performance-analysi-srcapp-k9vgz6.streamlit.app/" // URL of the Streamlit app
        width="100%"
        height="800px"
        title="Streamlit EDA"
        style={{ border: "none" }}
      />
    </div>
  );
}

export default EDA;
