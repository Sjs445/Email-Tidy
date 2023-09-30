import axios from 'axios';
import {useState} from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {toast} from 'react-toastify';
import { scanLinkedEmail, reset} from '../features/scanned_emails/scannedEmailSlice';


function ScanEmailForm({linked_email_id, setScannedEmailCount, setscanTaskId, setIsScanning}) {
    const dispatch = useDispatch();

    const { user } = useSelector( (state) => state.auth );

    const [formData, setFormData ] = useState({
        how_many: 10,
        linked_email_id: linked_email_id,
    });

    const { how_many } = formData;

    const onChange = (e) => {
        setFormData( (prevState) => ({
            ...prevState,
            [e.target.name]: e.target.value,
        }) )
    };

    const onSubmit = e => {
        e.preventDefault();
    
        if ( !how_many ) {
          return toast.error("Set an amount of emails to scan for");
        }
    
        const scanEmailData = { how_many, linked_email_id };

        setIsScanning(true);
        setScannedEmailCount(how_many);

        // TODO: Change this to be an async thunk method since the progress bar doesn't show up until this post is complete
        axios.post("/scanned_emails/", scanEmailData, { headers: { Authorization: `Bearer ${user}`}}).then( (response) => {
            setscanTaskId(response.data.task_id);
        }).catch( error => {
            toast.error(error.data.details);
        })
      }

  return <section className='form'>
    <form onSubmit={onSubmit}>
        <div className='form-group'>
            <label htmlFor='how_many'>Emails to Scan</label>
            <select name='how_many' id='how_many' onChange={onChange} value={how_many}>
                <option value={10}>10</option>
                <option value={20}>20</option>
                <option value={30}>30</option>
            </select>
            <button className='btn btn-block' type='submit'>Scan Emails</button>
        </div>
    </form>
  </section>
}

export default ScanEmailForm