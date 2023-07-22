import { useDispatch } from "react-redux";
import {deleteLinkedEmail} from '../features/linked_emails/linkedEmailSlice';

function LinkedEmail( {email} ) {
    const dispatch = useDispatch();

  return (
    <div className="email">
        <div>
            { new Date(email.insert_ts).toLocaleString('en-US')}
        </div>
        <h2>{email.email}</h2>
        <button className="close" onClick={() => dispatch(deleteLinkedEmail(
            email.id
        ))}>X</button>
    </div>
  )
}

export default LinkedEmail