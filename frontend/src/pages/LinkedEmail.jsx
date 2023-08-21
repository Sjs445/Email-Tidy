import axios from 'axios';
import {useState} from 'react';
import { useEffect } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import { test_token } from "../features/auth/authSlice";
import { useDispatch, useSelector } from 'react-redux';
import { getScannedEmails, scanLinkedEmail, unsubscribeFromLinks, reset} from '../features/scanned_emails/scannedEmailSlice';
import Spinner from '../components/Spinner';
import {toast} from 'react-toastify';

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

  const [formData, setFormData ] = useState([]);

  const onChange = (e) => {
    if ( e.target.checked ) {
      formData.push(e.target.value);
    } else {
      setFormData(formData.filter( (scanned_id) => scanned_id !== e.target.value))
    }
  };

const onSubmit = e => {
  e.preventDefault();

  if ( formData.length == 0 ) {
    return toast.error("No emails selected");
  }

  const unsubscribeData = {
    linked_email_address: linked_email,
    scanned_email_ids: formData,
    page: currentPage,
  }

  dispatch(unsubscribeFromLinks(unsubscribeData));
  };

  
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
  const paginate = (currentPage) => {
    setCurrentPage(currentPage);
    setFormData([]);
  }
  const seenCount = 10 * ( currentPage + 1 );

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
      <form onSubmit={onSubmit}>
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
                <input
                 type="checkbox"
                 id={scanned_email.id}
                 name={scanned_email.id}
                 value={scanned_email.id}
                 onChange={onChange} />
                <label htmlFor={scanned_email.id}>Unsubscribe</label>
                </div>
                : <p>{scanned_email.unsubscribe_status}</p>
            ) : <p>No unsubscribe links found</p>}
            </td>
        </tr>
    ))}
    </tbody>
    </table>

    {/* TODO: Add number links to go directly to a page */}

    {/* Don't allow someone to go to the previous page if we're on page 0*/}
    {currentPage === 0 ? <button className='btn' disabled>Prev Page</button> : <button className='btn'  onClick={ () => paginate(currentPage-1)}>Prev Page</button> }

    {/* Don't allow someone to go to the next page if we're at the max count of emails */}
    { seenCount < scannedEmailCount  ? <button className='btn' onClick={ () => paginate(currentPage+1)}>Next Page</button> : <button className='btn' disabled>Next Page</button>  }
    
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