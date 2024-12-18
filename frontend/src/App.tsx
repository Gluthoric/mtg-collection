import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { AppLayout } from './components/layout/AppLayout';

export function App() {
  return (
    <Router>
      <AppLayout />
    </Router>
  );
}

export default App;