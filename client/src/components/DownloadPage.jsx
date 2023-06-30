import React from 'react';

export default function DownloadPage() {
  const handleClick = () => {
    fetch('http://127.0.0.1:5000/download', { method: 'GET' })
      .then(response => {
        if (response.ok) {
          return response.blob(); // Convert the response to a Blob object
        } else {
          throw new Error('Download request failed!');
        }
      })
      .then(blob => {
        // Create a URL object from the Blob data
        const url = URL.createObjectURL(blob);

        // Create a temporary <a> element to trigger the file download
        const link = document.createElement('a');
        link.href = url;
        link.download = 'output.pdf'; // Specify the desired filename for the downloaded file
        link.click();

        // Clean up the URL object
        URL.revokeObjectURL(url);
      })
      .catch(error => {
        console.error('Download error:', error);
      });
  };

  return (
    <div>
      <h1>Download Page</h1>
      <button onClick={handleClick}>Download File</button>
    </div>
  );
}
