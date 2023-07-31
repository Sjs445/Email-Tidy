import { useEffect } from "react";
import {useNavigate} from 'react-router-dom';
import {useSelector, useDispatch} from 'react-redux';
import LinkedEmailForm from "../components/linkedEmailForm";
import LinkedEmail from "../components/linkedEmail";
import Spinner from '../components/Spinner';
import {getLinkedEmails, reset} from '../features/linked_emails/linkedEmailSlice';
import { test_token } from "../features/auth/authSlice";

function Dashboard() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const { user } = useSelector( (state) => state.auth );
  const { linked_emails, isLoading, isError, message } = useSelector( (state) => state.email)

  // If there's no user token send them to the login page.
  // If the token exists verify it's a valid token before fetching for linked emails.
  useEffect( () => {
    if (!user) {
      navigate('/login');
    } else {
      dispatch(test_token());
    }
    
  }, [navigate, dispatch, user])

  useEffect( () => {
    // Get a list of linked emails
    if ( user ) {
      dispatch(getLinkedEmails());
    }
    
    // When we leave the dashboard clear the linked emails state
    return () => {
      dispatch(reset());
    }
  }, [user, navigate, isError, message, dispatch])

  if ( isLoading ) {
    return <Spinner />
  }


  return( <>
  <section className='heading'>
    <h1>Welcome { user && user.email }</h1>
    <p>Linked Email Dashboard</p>
  </section>

  <section className="content">
    {linked_emails.length > 0 ? (
      <div className="linked_emails" >
        {linked_emails.map((email) => (
          <LinkedEmail key={email.id} email={email} />
        ))}
      </div>
    ) : (<h3>You have no linked emails</h3>)}
  </section>

  <LinkedEmailForm />
  </>
  )
}

export default Dashboard