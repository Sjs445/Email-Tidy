import { useEffect, useState } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import { test_token } from "../features/auth/authSlice";
import { useDispatch, useSelector } from 'react-redux';
import { getScannedEmails, unsubscribeFromLinks, unsubscribeFromAll, reset, getRunningTask, getScannedEmailCount} from '../features/scanned_emails/scannedEmailSlice';
import Spinner from '../components/Spinner';
import {toast} from 'react-toastify';
import UnsubscribeStatus from '../components/UnsubscribeStatus';
import ScanEmailForm from '../components/ScanEmailForm';
import ProgressBar from '../components/ProgressBar';

// TODO: Make this a page accessible by URL. When someone clicks on an email sender they are navigated here.
// On this page you should be able to:
//   1. See scanned emails using infinite scroll.
//   2. Be able to unsubscribe from this sender.
//   3. Be able to see the unsubscribe status per scanned email.
//   4. Be able to click scanned emails to see their unsubscribe links.
function ScannedEmails() {

  const navigate = useNavigate();
  const dispatch = useDispatch();
  const params = useParams();
  const [ searchParams ] = useSearchParams();
  const linked_email = searchParams.get("linked_email");
  const email_from   = searchParams.get("email_from");

  const { user } = useSelector( (state) => state.auth );
  const { scanned_emails, scan_task_id, unsubscribe_task_id, scanned_email_count, isLoading, isError, message } = useSelector( (state) => state.scanned_email);

  const [scanningDone, setScanningDone] = useState(false);
  const [page, setPage] = useState(0);

  // Unsubscribe from selected emails
  const onSubmit = e => {
    e.preventDefault();

    if ( formData.length == 0 ) {
      return toast.error("No emails selected");
    }

    const unsubscribeData = {
      linked_email_address: linked_email,
      email_sender: email_from,
      page: page,
    }

    dispatch(unsubscribeFromLinks(unsubscribeData));
    setFormData([]);
  };
  
  // If there's no user token send them to the login page.
  // If the token exists verify it's a valid token before fetching for linked emails.
  useEffect( () => {
    if (!user) {
      navigate('/login');
    } else {
      dispatch(test_token())
        .then( () => dispatch(getRunningTask(linked_email)))
        .then( () => dispatch(getScannedEmailCount(linked_email)) )
        .then( () => {
          const getScannedEmailData = {
            page: page,
            linked_email: linked_email
          }
          dispatch(getScannedEmails(getScannedEmailData));
        })
    }

    return () => {
      dispatch(reset());
    }
    
  }, [navigate, dispatch, user, page, scanningDone]);

  // Tells us how many scanned emails from this page we've seen
  const seenCount = 10 * ( page + 1 );

  // Number of pages
  const totalPages = Math.floor(scanned_email_count / 10);

  // Previous pages
  let prevPages = [];

  if ( page > 0 && page < totalPages ) {
    prevPages.push(page-1);
  }

  if ( isLoading ) {
    return <Spinner />
  }

  if ( scan_task_id || unsubscribe_task_id ) {
    return <ProgressBar setScanningDone={setScanningDone} linked_email={linked_email} />
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
      <button className="btn btn-block" onClick={unsubFromAll}>Unsubscribe From All</button>
      <table className='content-table'>
        <thead>
          <tr>
            <th>From</th>
            <th>Subject</th>
            <th>Unsubscribe Links Found</th>
            <th>Unsubscribe</th>
          </tr>
        </thead>
        <tbody>
        {scanned_emails.slice(0, 10).map( (scanned_email) => (
        <tr key={scanned_email.id}>
            <td>{scanned_email.from}</td>
            <td>{scanned_email.subject}</td>
            <td>{scanned_email.link_count}</td>
            <td>
            {scanned_email.link_count > 0 ? (
              scanned_email.unsubscribe_status === 'pending' ? 
                <div>
                <label className='checkbox' htmlFor={scanned_email.id}>
                  <input
                  className='checkbox__input'
                  type="checkbox"
                  id={scanned_email.id}
                  name={scanned_email.id}
                  value={scanned_email.id}
                  onChange={onChange} />
                  <div className='checkbox__box'></div>
                  Unsubscribe
                </label>
                </div>
                : <UnsubscribeStatus scanned_email_id={scanned_email.id} unsubscribe_status={scanned_email.unsubscribe_status} linked_email={linked_email} />
            ) : <p>No unsubscribe links found</p>}
            </td>
        </tr>
    ))}
    </tbody>
    </table>

    {/* TODO: Add number links to go directly to a page. */}

    <div style={{display: 'flex', justifyContent: 'space-between'}}>

    {/* Don't allow someone to go to the previous page if we're on page 0*/}
    { page === 0 ? 
      <button className='btn btn-prev' disabled>&laquo; Prev Page</button> : 
      <div>
        <button className='btn btn-prev' type="button" onClick={ () => navToPage(0)}>&laquo;</button>
        <button className='btn btn-prev' type="button" onClick={ () => navToPage(page-1)}>&laquo; Prev Page</button>
      </div>
    }

    {/* Don't allow someone to go to the next page if we're at the max count of emails */}
    { seenCount < scanned_email_count  ?
      <div>
        <button className='btn btn-next' type="button" onClick={ () => navToPage(page + 1)}>Next Page &raquo;</button>
        <button className='btn btn-next' type="button" onClick={ () => navToPage(totalPages)}>&raquo;</button>
      </div> : <button className='btn btn-next' disabled>Next Page &raquo;</button>
    }
    </div>
  
    <button type="submit" className='btn btn-block' style={{marginTop: '10px', marginBottom: '5px'}}>Unsubscribe</button>
    </form>
    ) : (
      <div>
        <h3>No scanned emails found.</h3>
        <ScanEmailForm linked_email_id={params.id} />
      </div>
    )}
    
    </section>
    </>
  )
}

export default ScannedEmails