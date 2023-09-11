// In the case the unsubscribe failed allow the user to query the backend for the unsubscribe links
// that were found. They can then try those links themselves since the reason for the failure
// is probably some user interaction is involved.
import Modal from './Modal';
import { useState } from 'react';

function UnsubscribeStaus( { scanned_email_id, unsubscribe_status, linked_email } ) {

  const [openModal, setOpenModal] = useState(false);

  const onClick = (e) => {
    e.preventDefault();
    setOpenModal(true);
  }

  return (
    <div>
        { unsubscribe_status === 'failure' ? (
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
            ) : unsubscribe_status === 'success' ? ( 
            <p style={{color: "green"}}>success</p>
            ) : <p>{unsubscribe_status}</p>
        }
    </div>
  )
}

export default UnsubscribeStaus