import { useEffect, useState } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import { test_token } from "../features/auth/authSlice";
import { useDispatch, useSelector } from 'react-redux';
import { getScannedEmails, unsubscribeFromLinks, reset, getRunningTask } from '../features/scanned_emails/scannedEmailSlice';
import Spinner from '../components/Spinner';
import {toast} from 'react-toastify';
import UnsubscribeStatus from '../components/UnsubscribeStatus';
import ProgressBar from '../components/ProgressBar';
import InfiniteScroll from 'react-infinite-scroll-component';


function ScannedEmails() {

  const navigate = useNavigate();
  const dispatch = useDispatch();
  const params = useParams();
  const [ searchParams ] = useSearchParams();
  const linked_email = searchParams.get("linked_email");
  const email_from   = params.sender;

  const { user } = useSelector( (state) => state.auth );
  const { scanned_emails, scan_task_id, unsubscribe_task_id, isLoading } = useSelector( (state) => state.scanned_email);

  const [scanningDone, setScanningDone] = useState(false);
  const [page, setPage] = useState(0);

  // Unsubscribe from this sender
  const onSubmit = e => {
    e.preventDefault();

    const unsubscribeData = {
      linked_email_address: linked_email,
      email_sender: email_from,
    }

    dispatch(unsubscribeFromLinks(unsubscribeData));
  };
  
  // If there's no user token send them to the login page.
  // If the token exists verify it's a valid token before fetching for linked emails.
  useEffect( () => {
    if (!user) {
      navigate('/login');
    } else {
      dispatch(test_token())
        .then( () => dispatch(getRunningTask(linked_email)))
        .then( () => {
          const getScannedEmailData = {
            page: page,
            linked_email: linked_email,
            email_from: email_from,
          }
          dispatch(getScannedEmails(getScannedEmailData));
        })
    }

    return () => {
      dispatch(reset());
    }
    
  }, [navigate, dispatch, user, scanningDone]);

  // Tells us how many scanned emails from this page we've seen
  const seenCount = 10 * ( page + 1 );
  const totalEmails = scanned_emails ? scanned_emails[0]?.total_count : 0;

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
      <div>
      <button onClick={onSubmit} className='btn btn-block'>Unsubscribe from {email_from}</button>
      <div id="scroll" style={{ height: 500, overflow: "auto" }}>
    
      <InfiniteScroll
        dataLength={scanned_emails.length}
        next={ () => {
          setPage(page+1);
          dispatch(getScannedEmails({linked_email: linked_email, page: page + 1, email_from: email_from}));
         }
        }
        hasMore={seenCount < totalEmails}
        loader={<p>Loading...</p>}
        scrollableTarget="scroll"
      >

      <table className='content-table'>
        <thead>
          <tr>
            <th>Subject</th>
            <th>Unsubscribe Links Found</th>
            <th>Unsubscribe Status</th>
          </tr>
        </thead>
        <tbody>
        {scanned_emails.map( (scanned_email) => (
        <tr key={scanned_email.id}>
            <td>{scanned_email.subject}</td>
            <td>{scanned_email.unsubscribe_link_count}</td>
            <td>
            {scanned_email.unsubscribe_link_count > 0 ? (
              <UnsubscribeStatus scanned_email_id={scanned_email.id} unsubscribe_statuses={scanned_email.unsubscribe_statuses} linked_email={linked_email} />
            ) : <p>No unsubscribe links found</p>}
            </td>
        </tr>
    ))}
    </tbody>
    </table>
    </InfiniteScroll>
    </div>
    </div>
    ) : (
      <div>
        <h3>No scanned emails found.</h3>
      </div>
    )}
    
    </section>
    </>
  )
}

export default ScannedEmails