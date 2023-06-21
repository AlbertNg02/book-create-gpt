import React from 'react';

const DataRequestForm = () => {
  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission logic here
  };

  return (
    <div>
      <h2>Data Request</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="prompt">Prompt:</label>
        <input type="text" name="prompt" id="prompt" required />
        <br />
        <label htmlFor="chapters_number">Number of Chapters:</label>
        <input type="number" name="chapters_number" id="chapters_number" required />
        <br />
        <label htmlFor="api_key">API Key:</label>
        <input type="password" name="api_key" id="api_key" autoComplete="off" required style={{ width: '300px' }} />
        <br />
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
};

export default DataRequestForm;
