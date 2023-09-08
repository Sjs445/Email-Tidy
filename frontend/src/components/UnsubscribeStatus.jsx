// In the case the unsubscribe failed allow the user to query the backend for the unsubscribe links
// that were found. They can then try those links themselves since the reason for the failure
// is probably some user interaction is involved.
import Modal from './Modal';
import { useState } from 'react';

function UnsubscribeStaus( { scanned_email_id, unsubscribe_status } ) {

  const [openModal, setOpenModal] = useState(false);

  const onClick = (e) => {
    e.preventDefault();
    setOpenModal(true);
  }

  return (
    <div>
        { unsubscribe_status === 'failure' ? (
               <div style={{margin: 'auto', width: '75%'}}>
                <p style={{ color: "red"}}>failed</p>
                <button onClick={onClick} className="btn" style={{marginBottom: '5px'}}>See Links</button>
                <Modal 
      open={openModal} 
      onClose={() => setOpenModal(false)} />
                </div>
            ) : unsubscribe_status === 'success' ? ( 
            <p style={{color: "green"}}>success</p>
            ) : <p>{unsubscribe_status}</p>
        }
    </div>
  )
}

export default UnsubscribeStaus