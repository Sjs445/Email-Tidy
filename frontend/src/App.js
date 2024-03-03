import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Header from './components/Headers';
import Dashboard from './pages/Dashboard';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import LinkedEmail from './pages/LinkedEmail';
import ScannedEmails from './pages/ScannedEmails';

function App() {
  return (
    <>
    <Router>
    <div className='container'>
      <Header />
      <Routes>
        <Route path='/' element={<Dashboard />} />
        <Route path='/getting-started' element={<Landing /> } />
        <Route path='/login' element={<Login />} />
        <Route path='/register' element={<Register />} />
        <Route path='/linked_email/:id' element={<LinkedEmail />} />
        <Route path='/scanned_emails/:sender' element={<ScannedEmails />} />
        <Route path='/*' element={ <Navigate to="/" /> } />
      </Routes>
    </div>
    </Router>
    <ToastContainer />
    </>
  );
}

export default App;
