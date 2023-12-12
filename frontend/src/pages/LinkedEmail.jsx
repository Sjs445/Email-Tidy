import { useEffect, useState } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import { test_token } from "../features/auth/authSlice";
import { useDispatch, useSelector } from 'react-redux';
import { getEmailSenders, unsubscribeFromAll, unsubscribeFromLinks, reset, getRunningTask } from '../features/scanned_emails/scannedEmailSlice';
import Spinner from '../components/Spinner';
import {toast} from 'react-toastify';
import ScanEmailForm from '../components/ScanEmailForm';
import ProgressBar from '../components/ProgressBar';
import InfiniteScroll from 'react-infinite-scroll-component';


function LinkedEmail() {

  const navigate = useNavigate();
  const dispatch = useDispatch();
  const params = useParams();
  const [ searchParams ] = useSearchParams();
  const linked_email = searchParams.get("linked_email");

  const { user } = useSelector( (state) => state.auth );
  const { email_senders, scan_task_id, unsubscribe_task_id, isLoading, isError, message } = useSelector( (state) => state.scanned_email);

  const [scanningDone, setScanningDone] = useState(false);
  const [page, setPage] = useState(0);

  // Unsubscribe from all emails
  const unsubFromAll = (e) => {
    e.preventDefault();

    const unsubscribeData = {
      linked_email_address: linked_email,
    }

    dispatch(unsubscribeFromAll(unsubscribeData));
  };
  
  // If there's no user token send them to the login page.
  // If the token exists verify it's a valid token before fetching for email senders.
  useEffect( () => {
    if (!user) {
      navigate('/login');
    } else {
      dispatch(test_token())
        .then( () => dispatch(getRunningTask(linked_email)))
        .then( () => {
          const getEmailSenderData = {
            page: page,
            linked_email: linked_email
          }
          dispatch(getEmailSenders(getEmailSenderData));
        })
    }

    return () => {
      dispatch(reset());
    }
    
  }, [navigate, dispatch, user, scanningDone]);

  // Tells us how many email senders from this page we've seen
  const seenCount = 10 * ( page + 1 );
  const totalSenders = email_senders ? email_senders[0]?.total_count : 0;

  if ( isLoading ) {
    return <Spinner />
  }

  if ( scan_task_id || unsubscribe_task_id ) {
    return <ProgressBar setScanningDone={setScanningDone} linked_email={linked_email} />
  }

  return (
    <>
    <section className="heading">
    <h1>Spam Email Senders</h1>
    <p>{linked_email}</p>
    </section>
    
    <section>
    {email_senders.length > 0 ? (
    <div>
      <h3>You may unsubscribe from all spam email senders here or inspect individual senders</h3>
    <button className="btn btn-block" onClick={unsubFromAll}>Unsubscribe From All Emails</button>
    <div id="scroll" style={{ height: 500, overflow: "auto" }}>
    
    <InfiniteScroll
      dataLength={email_senders.length}
      next={ () => {
        setPage(page+1);
        dispatch(getEmailSenders({linked_email: linked_email, page: page + 1}));
       }
      }
      hasMore={seenCount < totalSenders}
      loader={<p>Loading...</p>}
      scrollableTarget="scroll"
    >
      <table className='content-table' >
      <thead>
        <tr>
          <th>From</th>
          <th>Total Scanned Emails</th>
          <th>Unqiue Unsubscribe Links Found</th>
        </tr>
      </thead>
      <tbody>
        {email_senders.map( (email_sender) => (   
        <tr key={email_sender.email_from}>
            <td>{email_sender.email_from}</td>
            <td>{email_sender.scanned_email_count}</td>
            <td>{email_sender.unsubscribe_link_count}</td>
            {/* TODO: Add button here to click and navigate to see this email sender's scanned emails */}
        </tr>
        ))}
      </tbody>
      </table>
    </InfiniteScroll>
      </div>
      </div>
    ) : (
      <div>
        <h3>No Spam Found</h3>
        <ScanEmailForm linked_email_id={params.id} />
      </div>
    )}
    
    </section>
    </>
  )
}

export default LinkedEmail