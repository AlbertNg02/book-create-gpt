import { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Outlet, Link, Route, Routes} from "react-router-dom";

import InputHandler from './components/InputHandler';
import DownloadPage from './components/DownloadPage';

function App() {
  

  return (
    <Routes>
      <Route path="/" element={<InputHandler />}/>
      <Route path="/download" element={<DownloadPage />}/>
    </Routes>
  );
}

export default App;
