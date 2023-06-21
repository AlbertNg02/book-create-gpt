import React, { useState } from 'react';
import DataRequestForm from './components/DataRequestForm';
import DisplayComponent from './components/DisplayComponent';

const App = () => {
  const [formData, setFormData] = useState(null);

  const handleFormSubmit = (data) => {
    // Process the form data here (e.g., make API calls, perform computations)
    setFormData(data);
  };

  return (
    <div>
      {formData ? (
        <DisplayComponent formData={formData} />
      ) : (
        <DataRequestForm onSubmit={handleFormSubmit} />
      )}
    </div>
  );
};

export default App;
