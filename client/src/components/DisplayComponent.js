import React, { useEffect } from 'react';
import io from 'socket.io-client';
import Chart from 'chart.js/auto';

const DisplayComponent = () => {
  useEffect(() => {
    const socket = io('127.0.0.1:5000');

    socket.on('connect', () => {
      console.log('Connected to server!');
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from server');
    });

    socket.on('output_update', (data) => {
      console.log('Received data packet', data);
      document.getElementById('content').innerHTML = data.output;
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  useEffect(() => {
    const ctx = document.getElementById('chart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [
          {
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }, []);

  return (
    <div className="container">
      <div className="output-rectangle">
        <div className="output-container">
          <div id="content">Placeholder</div>
        </div>
        <div className="download-button">
          <a href="/download" className="centered-link">
            Download Output
          </a>
        </div>
      </div>
      <canvas id="chart" width="400" height="400"></canvas>
    </div>
  );
};

export default DisplayComponent;
