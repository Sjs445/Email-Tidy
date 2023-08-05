import { useDispatch } from "react-redux";
import {deleteLinkedEmail} from '../features/linked_emails/linkedEmailSlice';
import { useNavigate } from "react-router-dom";

function LinkedEmail( {email} ) {
    const dispatch = useDispatch();
    const navigate = useNavigate();

  return (
    <div className="email">
        <div>
            Linked on { new Date(email.insert_ts).toLocaleString('en-US')}
        </div>
        <h2>{email.email}</h2>
        <button className="btn btn-block" onClick={() => navigate('/linked_email/' + email.id + `?linked_email=${email.email}`) }>View</button>
        <button className="close" onClick={() => dispatch(deleteLinkedEmail(
            email.id
        ))}>X</button>
    </div>
  )
}

export default LinkedEmail