import { useDispatch } from "react-redux";
import {deleteLinkedEmail} from '../features/linked_emails/linkedEmailSlice';

function LinkedEmail( {email} ) {
    const dispatch = useDispatch();

    /*
    TODO: Add button on the linked email, which navigates them to a new page. That new page fetches scanned email data for this specific linked email address.
        
    It should call a get request to /linked_email/0?linked_email=<LINKED_EMAIL_ADDRESS>. Then display that information received.
    
    It should also allow for an option to scan emails for that linked email.
    */

  return (
    <div className="email">
        <div>
            Linked on { new Date(email.insert_ts).toLocaleString('en-US')}
        </div>
        <h2>{email.email}</h2>
        <button className="close" onClick={() => dispatch(deleteLinkedEmail(
            email.id
        ))}>X</button>
    </div>
  )
}

export default LinkedEmail