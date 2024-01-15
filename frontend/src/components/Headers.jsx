import { FaSignInAlt, FaSignOutAlt, FaUser, FaArrowLeft } from 'react-icons/fa'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux';
import {logout, reset} from '../features/auth/authSlice';



function Headers() {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const location = useLocation();
    
    const  { user } = useSelector( (state) => state.auth);

    const onLogout = () => {
        dispatch(logout());
        dispatch(reset());
        navigate('/login');
    }

  return (
    <header className='header'>
        <div className='logo'>
            <Link to='/'>EmailTidy</Link>
        </div>
        <div>
            {!user || location.pathname === '/' ? <></> : <button className='btn' onClick={ () => navigate(-1)}><FaArrowLeft /> Go Back </button>}
        </div>
        <ul>
            {user ? (
                <li>
                <button className='btn' onClick={onLogout}>
                    <FaSignOutAlt /> Logout
                </button>
            </li>
            ) : (<>
            <li>
            <Link to='/login'>
                <FaSignInAlt /> Login
            </Link>
        </li>
        <li>
            <Link to='/register'>
                <FaUser /> Register
            </Link>
        </li>
            </>) }
            
        </ul>
    </header>
  )
}

export default Headers