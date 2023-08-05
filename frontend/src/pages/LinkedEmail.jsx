import { useEffect } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import { test_token } from "../features/auth/authSlice";
import { useDispatch, useSelector } from 'react-redux';
import { getScannedEmails, scanLinkedEmail, reset} from '../features/scanned_emails/scannedEmailSlice';
import Spinner from '../components/Spinner';


function LinkedEmail() {

  const navigate = useNavigate();
  const dispatch = useDispatch();
  const params = useParams();
  const [ searchParams ] = useSearchParams();
  const linked_email = searchParams.get("linked_email");

  const { user } = useSelector( (state) => state.auth );
  const { scanned_emails, isLoading, isError, message } = useSelector( (state) => state.scanned_email)
  
  // If there's no user token send them to the login page.
  // If the token exists verify it's a valid token before fetching for linked emails.
  useEffect( () => {
    if (!user) {
      navigate('/login');
    } else {
      dispatch(test_token());
    }
    
  }, [navigate, dispatch, user])

  // We should check that this url is valid. Maybe if the email id is not valid, return them to
  // the dashboard.
  useEffect( () => {

    if ( user ) {
      const getScannedEmailData = {
        page: 0,
        linked_email: linked_email
      }
      dispatch(getScannedEmails(getScannedEmailData));
    }

    // When we leave the dashboard clear the scanned_emails state
    return () => {
      dispatch(reset());
    }
  }, []);

  if ( isLoading ) {
    return <Spinner />
  }

  return (
    <>
    <section className="heading">
    <h1>Scanned Emails</h1>
    <p>{linked_email}</p>
    </section>
    
    <section className="content">
    {scanned_emails.length > 0 ? (
      <div>
        {scanned_emails.map( (scanned_email) => (
      <pre>{JSON.stringify(scanned_email)}</pre>
    ))}
      </div>
    ) : (
    <h3>No scanned emails found.</h3>
    )}
    <button className="btn btn-block" onClick={() => dispatch(scanLinkedEmail({linked_email_id: params.id, how_many: 20}))}>Scan 20 Emails for Spam</button>
    </section>
    </>
  )
}

export default LinkedEmail