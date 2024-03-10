import { useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getTaskStatus, clearTaskId, updateTaskStatus } from '../features/scanned_emails/scannedEmailSlice';

// This component is shared by scanned tasks and unsubscribe tasks. Note the ternary statements.
function ProgressBar({setScanningDone, linked_email}) {
  
  const { scan_task_id, unsubscribe_task_id, progress } = useSelector( (state) => state.scanned_email);
  const filled = progress.filled ? progress.filled : 0;

  const dispatch = useDispatch();

	useEffect(() => {
    if ( filled < 100 ) {
        dispatch(getTaskStatus(scan_task_id ? scan_task_id : unsubscribe_task_id))
          .then( () => {
              setTimeout( () => dispatch(updateTaskStatus()), 1500);
          });
    } else {
        setScanningDone(true);
        dispatch(clearTaskId());
    }
	},[progress, dispatch]);

  return (
	  <section className='form'>
        { scan_task_id ? 
          <h1>Scanning emails for {linked_email}</h1>
           : <h1>Unsubscribing from emails for {linked_email}</h1>
        }
        <p>This may take a while. Feel free to close this page and come back later.</p>
		  <div className="progressbar">
			  <div style={{
				  height: "100%",
				  width: `${filled}%`,
				  backgroundColor: "#000000",
				  transition:"width 0.5s"
			  }}></div>
              <span className="progressPercent">{ filled }%</span>
		  </div>
	</section>
  )
}

export default ProgressBar