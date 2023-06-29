import React from 'react';

class DownloadPage extends React.Component {
  handleClick = () => {
    fetch('/download', { method: 'GET' }) // Change '/download' to the appropriate Flask route
      .then(response => {
        if (response.ok) {
          // Handle success response from the server
          console.log('Download request succeeded!');
          // You can perform additional actions here, such as downloading the file
        } else {
          // Handle error response from the server
          console.error('Download request failed!');
        }
      })
      .catch(error => {
        // Handle network error
        console.error('Network error:', error);
      });
  }

  render() {
    return (
      <div>
        <h1>Download Page</h1>
        <button onClick={this.handleClick}>Download File</button>
      </div>
    );
  }
}

export default DownloadPage;
