import { useDispatch } from 'react-redux';
import { scanLinkedEmail } from '../features/scanned_emails/scannedEmailSlice';


function ScanEmailForm({linked_email_id, rescan}) {
    const dispatch = useDispatch();

    const scan = rescan ? "Re-scan" : "Scan"

    const onSubmit = e => {
        e.preventDefault();

        const scanEmailData = { linked_email_id };

        dispatch(scanLinkedEmail(scanEmailData));
      }

  return <section className='form'>
    <form onSubmit={onSubmit}>
        <div className='form-group'>
            <button className='btn btn-block' type='submit'>{scan} All Emails</button>
        </div>
    </form>
  </section>
}

export default ScanEmailForm