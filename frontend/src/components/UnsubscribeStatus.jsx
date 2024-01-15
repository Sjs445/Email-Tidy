// In the case the unsubscribe failed allow the user to query the backend for the unsubscribe links
// that were found. They can then try those links themselves since the reason for the failure
// is probably some user interaction is involved.
import Modal from './Modal';
import { useState } from 'react';

function UnsubscribeStatus( { scanned_email_id, unsubscribe_statuses, linked_email } ) {

  const [openModal, setOpenModal] = useState(false);

  const onClick = (e) => {
    e.preventDefault();
    setOpenModal(true);
  }

  return (
    <div>
        { unsubscribe_statuses.every( (status) => status === 'failure') ? (
               <div>
                <p style={{ color: "red"}}>failed</p>
                <button type='button' className='button' onClick={onClick} style={{marginBottom: '5px'}}>
                <span className='button__text'>View Links</span>
                <span className='button__icon'>
                <ion-icon name="ellipsis-vertical-outline"></ion-icon>
                </span>
                
                </button>
                <Modal 
      open={openModal} 
      onClose={() => setOpenModal(false)}
      scanned_email_id={scanned_email_id}
      linked_email={linked_email} />
                </div>
            ) : unsubscribe_statuses.every( (status) => status === 'success') ? ( 
            <div>
              <p style={{color: "green"}}>success</p>
              <button type='button' className='button' onClick={onClick} style={{marginBottom: '5px'}}>
                <span className='button__text'>View Links</span>
                <span className='button__icon'>
                <ion-icon name="ellipsis-vertical-outline"></ion-icon>
                </span>
                
                </button>
                <Modal 
      open={openModal} 
      onClose={() => setOpenModal(false)}
      scanned_email_id={scanned_email_id}
      linked_email={linked_email} />
            </div>
            ) : <div>
            <p style={{color: "orange"}}>Success and Failed</p>
            <button type='button' className='button' onClick={onClick} style={{marginBottom: '5px'}}>
                <span className='button__text'>View Links</span>
                <span className='button__icon'>
                <ion-icon name="ellipsis-vertical-outline"></ion-icon>
                </span>
                
                </button>
                <Modal 
      open={openModal} 
      onClose={() => setOpenModal(false)}
      scanned_email_id={scanned_email_id}
      linked_email={linked_email} />
            </div>
        }
    </div>
  )
}

export default UnsubscribeStatus