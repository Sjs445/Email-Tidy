import axios from 'axios';
import {useState} from 'react';
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

  const [currentPage, setCurrentPage] = useState(0);
  const [scannedEmailCount, setScannedEmailCount] = useState(0);

  
  // If there's no user token send them to the login page.
  // If the token exists verify it's a valid token before fetching for linked emails.
  useEffect( () => {
    const fetch_count = async () => {
      const res = await axios.get(`/scanned_emails/count/${linked_email}`,
      { headers: {
        Authorization: `Bearer ${user}`
        }
      },
    )
    setScannedEmailCount(res.data.count)
    };

    if (!user) {
      navigate('/login');
    } else {
      dispatch(test_token())
        .then( () => {

          fetch_count();
          console.log("scanned email count " + scannedEmailCount)
          console.log("current page" + currentPage)

          
          const getScannedEmailData = {
            page: currentPage,
            linked_email: linked_email
          }
          
          dispatch(getScannedEmails(getScannedEmailData));
        })
        .catch( (error) => {
          console.log(error)
        })
    }

    return () => {
      dispatch(reset());
    }
    
  }, [navigate, dispatch, user, currentPage])

  // Paginate the data table
  const paginate = currentPage => setCurrentPage(currentPage);

  // TODO: We should check that this url is valid. Maybe if the email id is not valid or they do not
  // own the email, return them to the dashboard.

  if ( isLoading ) {
    return <Spinner />
  }

  return (
    <>
    <section className="heading">
    <h1>Scanned Emails</h1>
    <p>{linked_email}</p>
    </section>
    
    <section>
    {scanned_emails.length > 0 ? (
      <form>
      <table>
        <thead>
          <tr>
              <th>From</th>
              <th>Subject</th>
              <th>Unsubscribe Links Found</th>
              <th>Unsubscribe</th>
            </tr>
        </thead>
        <tbody>
        {scanned_emails.map( (scanned_email) => (   
        <tr key={scanned_email.id}>
            <td>{scanned_email.from}</td>
            <td>{scanned_email.subject}</td>
            <td>{scanned_email.link_count}</td>
            <td>
            {scanned_email.link_count > 0 ? (
              scanned_email.unsubscribe_status === 'pending' ? 
                <div>
                <input type="checkbox" id={scanned_email.id} name={scanned_email.id} value={scanned_email.id} />
                <label htmlFor={scanned_email.id}>Unsubscribe</label>
                </div>
                : <p>{scanned_email.unsubscribe_status}</p>
            ) : <p>No unsubscribe links found</p>}
            </td>
        </tr>
    ))}
    </tbody>
    </table>
    {currentPage === 0 ? <button className='btn' disabled>Prev Page</button> : <button className='btn'  onClick={ () => paginate(currentPage-1)}>Prev Page</button> }

    {/* TODO: Fetch a count of scanned emails and disable the next page button on max page */}
    <button className='btn' onClick={ () => paginate(currentPage+1)}>Next Page</button>
    <button type="submit" className='btn btn-block'>Unsubscribe</button>
    </form>
    ) : (
      <div>
        <h3>No scanned emails found.</h3>
        <button className="btn btn-block" onClick={() => dispatch(scanLinkedEmail({linked_email_id: params.id, how_many: 10}))}>Scan 10 Emails for Spam</button>
      </div>
    )}
    
    </section>
    </>
  )
}

export default LinkedEmail