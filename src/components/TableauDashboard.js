import React, { useEffect } from 'react';
import './TableauDashboard.css'; // Assuming you have a CSS file for styling

function TableauDashboard() {
  useEffect(() => {
    const divElement = document.getElementById('viz1729527875652');
    const vizElement = divElement.getElementsByTagName('object')[0];
    
    // Set dimensions based on the specified width and height
    vizElement.style.width = '1169px';
    vizElement.style.height = '827px';

    const scriptElement = document.createElement('script');
    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
    vizElement.parentNode.insertBefore(scriptElement, vizElement);
  }, []);

  return (
    <div className="tableau-container">
      <div className="tableauPlaceholder" id="viz1729527875652" style={{ position: 'relative' }}>
        <noscript>
          <a href="#">
            <img alt="Dashboard" src="https://public.tableau.com/static/images/Fi/Finalproject1tableau/Dashboard2/1_rss.png" style={{ border: 'none' }} />
          </a>
        </noscript>
        <object className="tableauViz" style={{ display: 'none' }}>
          <param name="host_url" value="https%3A%2F%2Fpublic.tableau.com%2F" />
          <param name="embed_code_version" value="3" />
          <param name="site_root" value="" />
          <param name="name" value="Finalproject1tableau/Dashboard2" />
          <param name="tabs" value="no" />
          <param name="toolbar" value="yes" />
          <param name="static_image" value="https://public.tableau.com/static/images/Fi/Finalproject1tableau/Dashboard2/1.png" />
          <param name="animate_transition" value="yes" />
          <param name="display_static_image" value="yes" />
          <param name="display_spinner" value="yes" />
          <param name="display_overlay" value="yes" />
          <param name="display_count" value="yes" />
          <param name="language" value="en-US" />
        </object>
      </div>
    </div>
  );
}

export default TableauDashboard;
