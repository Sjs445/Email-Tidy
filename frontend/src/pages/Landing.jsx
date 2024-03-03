import { useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import emailImage from '../assets/email_1920.png';

function Landing() {

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const { user } = useSelector( (state) => state.auth );

  // If there's a user token send them to the dashboard
  useEffect( () => {
    if (user) {
      navigate('/');
    }
    
  }, [navigate, dispatch]);

  return (
    <div>
        <h1>Welcome to <span style={{fontWeight:'normal'}}>EmailTidy</span></h1>
        <h2 style={{fontWeight:'normal'}}>Take control back over your inbox by allowing our app to scan for spam and automatically unsubscribe from unwanted junk mail.</h2>
        <div style={{justifyContent:'center', display:'flex', alignItems:'center', marginBottom:'10px'}}>
        <img src={emailImage} alt="junk email" style={{maxHeight: '600px', maxWidth: '600px'}} />
        </div>
        <div style={{justifyContent:'center', display:'flex', alignItems:'center'}}>
            <button className="btn" onClick={ () => navigate('/register')}>Get Started</button>
        </div>
        
        
        
    </div>
  )
}

export default Landing
