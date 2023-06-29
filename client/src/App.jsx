import { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Outlet, Link, Route, Routes} from "react-router-dom";

import InputHandler from './components/InputHandler';

function App() {
  

  return (
    <Routes>
      <Route path="/" element={<InputHandler />}/>
    </Routes>
  );
}

export default App;
