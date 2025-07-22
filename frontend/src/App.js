import React, { useState, useEffect } from 'react';
import DriveSelection from './components/DriveSelection';
import RecoverySettings from './components/RecoverySettings';
import io from 'socket.io-client';

const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
const socket = io(backendUrl.replace(/^http/, 'ws'), { secure: true });

function App() {
  const [recoveryUpdates, setRecoveryUpdates] = useState([]);
  const [selectedDrive, setSelectedDrive] = useState(null);
  const [recoveryStatus, setRecoveryStatus] = useState('idle');

  useEffect(() => {
    socket.on('recovery_update', (message) => {
      setRecoveryUpdates(currentUpdates => [...currentUpdates, message]);
    });

    return () => {
      socket.off('recovery_update');
    };
  }, []);

  const handleDriveSelection = (drive) => {
    setSelectedDrive(drive);
  };

  const startRecovery = () => {
    if (!selectedDrive) {
      alert('Please select a drive first.');
      return;
    }

    fetch(`${backendUrl}/start_recovery`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ drive_path: selectedDrive.path }),
    })
    .then(response => {
      if (response.ok) {
        setRecoveryStatus('in_progress');
      } else {
        alert('Failed to start recovery process.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred.');
    });
  };

  return (
    <div>
      <DriveSelection onDriveSelect={handleDriveSelection} />
      <RecoverySettings />
      <button onClick={startRecovery}>Start Recovery</button>
      {recoveryStatus === 'in_progress' && <p>Recovery in progress...</p>}
      <div className="recovery-updates">
        {recoveryUpdates.map((update, index) => (
          <p key={index}>{update}</p>
        ))}
      </div>
    </div>
  );
}

export default App;
