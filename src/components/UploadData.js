import React, { useState } from 'react';
import './UploadData.css';

function UploadData() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    const uploadedFile = event.target.files[0];
    setFile(uploadedFile);
  };

  const handleUpload = () => {
    if (file) {
      // Here, we would ideally upload the file to a server
      // For now, we'll just redirect to the Streamlit app
      window.open('http://localhost:8501', '_self'); // Open Streamlit app in a new tab
    }
  };

  return (
    <div className="upload-data">
      <h1>Upload Data</h1>
      <div className="upload-container">
        <label className="file-input-label">
          Choose File
          <input type="file" accept=".csv" onChange={handleFileChange} />
        </label>
        {file && <div className="file-name">Selected file: {file.name}</div>}
        <button onClick={handleUpload}>Upload</button>
      </div>
    </div>
  );
}

export default UploadData;
