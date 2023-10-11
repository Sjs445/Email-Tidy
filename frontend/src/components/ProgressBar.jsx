import axios from 'axios';
import {useState, useEffect} from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { toast } from 'react-toastify';
import { reset } from '../features/scanned_emails/scannedEmailSlice';

function ProgressBar({auth_header, setIsScanning}) {
    
    const { task_id } = useSelector( (state) => state.scanned_email);

    const [isRunning, setIsRunning] = useState(task_id ? true : false);
    const [filled, setFilled] = useState(0);
    const [waitAttempts, setWaitAttempts] = useState(0);
    const [pollCount, setPollCount] = useState(0);

    const dispatch = useDispatch();

	useEffect(() => {

		if (isRunning && waitAttempts < 15 && filled < 100) {
            axios.get(`/scanned_emails/task_status/${task_id}`, { headers: auth_header}).then( (response) => {

                if ( response.data.state === 'PROGRESS') {
                    const total = response.data.details.total;
                    const current = response.data.details.current;
                    const filled_percent = (current/total) * 100;

                    setFilled(filled_percent);
                    setTimeout(() => setPollCount(pollCount+1), 1000);
                }
                else if ( response.data.state === 'FAILURE') {
                    setIsRunning(false);
                    setIsScanning(false);
                    toast.error('An error occurred while scanning your inbox');
                }
                else if ( response.data.state === 'SUCCESS') {
                    setFilled(100);
                    setIsRunning(false);
                    setIsScanning(false);

                    return () => {
                        dispatch(reset());
                    }
                }
                else {
                    setTimeout(() => setWaitAttempts(waitAttempts+1), 1000);
                }
            }).catch( error => {
                toast.error(error.data.detail || 'Encountered an error');
            })
		} else {
            setIsScanning(false);
        }
	},[isRunning, waitAttempts, pollCount, dispatch])
  return (
	  <div>
        <h1>Scanning emails</h1>
		  <div className="progressbar">
			  <div style={{
				  height: "100%",
				  width: `${filled}%`,
				  backgroundColor: "#a66cff",
				  transition:"width 0.5s"
			  }}></div>
			  <span className="progressPercent">{ filled }%</span>
		  </div>
	</div>
  )
}

export default ProgressBar