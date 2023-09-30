import axios from 'axios';
import {useState, useEffect} from 'react';
import { toast } from 'react-toastify';

function ProgressBar({task_id, auth_header, setScanTaskId, setIsScanning}) {
    const [filled, setFilled] = useState(0);
	const [isRunning, setIsRunning] = useState(task_id ? true : false);
    const [waitAttempts, setWaitAttempts] = useState(0);
    const [pollCount, setPollCount] = useState(0);
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
                else if ( response.data.state === 'SUCCESS') {
                    setFilled(100);
                    setIsRunning(false);
                    setIsScanning(false);
                    setScanTaskId(null);
                }
                else {
                    setTimeout(() => setWaitAttempts(waitAttempts+1), 1000);
                }
            }).catch( error => {
                toast.error(error)
            })
		} else {
            setScanTaskId(null);
            setIsScanning(false);
        }
	},[isRunning, waitAttempts, pollCount])
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