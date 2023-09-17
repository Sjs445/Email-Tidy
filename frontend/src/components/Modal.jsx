import { useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux';
import Spinner from '../components/Spinner';
import { getUnsubscribeLinks, reset} from '../features/unsubscribe_links/unsusbscribeLinkSlice';

function Modal({open, onClose, scanned_email_id, linked_email}) {

  const dispatch = useDispatch();

  const { unsubscribe_links, isLoading, isError, message } = useSelector( (state) => state.unsubscribe_links);

  const { user } = useSelector( (state) => state.auth );

    useEffect( () => {

      if ( !open ) {
        return;
      }

      const unsubscribeLinkData = {
        scanned_email_id: scanned_email_id,
        linked_email: linked_email,
      }


      dispatch(getUnsubscribeLinks(unsubscribeLinkData, user));

      return () => {
        dispatch(reset());
      };
    }, [dispatch, open])

    if (!open) return null;

    if ( isLoading ) {
      return <Spinner />
    }

    return (
      <div onClick={onClose} className='overlay'>
        <div
          onClick={(e) => {
            e.stopPropagation();
          }}
          className='modalContainer'
        >
          <div className='modalRight'>
            <p className='closeBtn' onClick={onClose}>
              X
            </p>
            <div className='content'>
              <h2>Unsubscribe Links</h2>
              <ol>
              {unsubscribe_links.links?.map( ( link ) => (
                <li key={link.id}><a href={link.link} target="_blank">{
                  link.link.length > 100 ? link.link.slice(0, 100) : link.link
                }</a></li>
              ))}
              </ol>
            </div>
          </div>
        </div>
      </div>
    );
}

export default Modal