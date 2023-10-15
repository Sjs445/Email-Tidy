import { useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getTaskStatus, reset, updateTaskStatus } from '../features/scanned_emails/scannedEmailSlice';

function ProgressBar({setScanningDone}) {
    
    const { task_id, progress } = useSelector( (state) => state.scanned_email);

    const filled = progress.filled ? progress.filled : 0;

    const dispatch = useDispatch();

	useEffect(() => {
        if ( filled < 100 ) {
            dispatch(getTaskStatus(task_id))
                .then( () => {
                    setTimeout( () => dispatch(updateTaskStatus()), 1000);
                });
        } else {
            setScanningDone(true);
            dispatch(reset()); 
        }
	},[progress, dispatch])
  return (
	  <section className='form'>
        <h1>Scanning emails</h1>
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