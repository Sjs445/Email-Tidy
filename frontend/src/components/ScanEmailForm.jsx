import { useDispatch } from 'react-redux';
import { scanLinkedEmail } from '../features/scanned_emails/scannedEmailSlice';


function ScanEmailForm({linked_email_id}) {
    const dispatch = useDispatch();

    const onSubmit = e => {
        e.preventDefault();

        const scanEmailData = { linked_email_id };

        dispatch(scanLinkedEmail(scanEmailData));
      }

  return <section className='form'>
    <form onSubmit={onSubmit}>
        <div className='form-group'>
            <button className='btn btn-block' type='submit'>Scan All Emails</button>
        </div>
    </form>
  </section>
}

export default ScanEmailForm