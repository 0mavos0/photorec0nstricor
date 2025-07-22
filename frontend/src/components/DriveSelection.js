import React, { useState, useEffect } from 'react';

const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

function DriveSelection({ onDriveSelect }) {
  const [drives, setDrives] = useState([]);
  const [selected, setSelected] = useState('');

  useEffect(() => {
    fetch(`${backendUrl}/drives`)
      .then(res => res.json())
      .then(data => setDrives(data))
      .catch(err => console.error('Failed to fetch drives', err));
  }, []);

  const handleChange = (e) => {
    const path = e.target.value;
    setSelected(path);
    if (onDriveSelect) {
      onDriveSelect({ path });
    }
  };

  return (
    <div>
      <label htmlFor="drive-select">Select Drive: </label>
      <select id="drive-select" value={selected} onChange={handleChange}>
        <option value="" disabled>Select drive...</option>
        {drives.map((d) => (
          <option key={d} value={d}>{d}</option>
        ))}
      </select>
    </div>
  );
}

export default DriveSelection;
