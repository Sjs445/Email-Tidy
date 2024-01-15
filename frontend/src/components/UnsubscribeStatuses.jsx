import { useNavigate } from 'react-router-dom';

function UnsubscribeStatuses({ statuses, email_from, linked_email}) {

    const navigate = useNavigate();

    const onClick = (e) => {
        e.preventDefault();

        navigate(`/scanned_emails/${email_from}?linked_email=${linked_email}`);
    }

    return (
        <div>
            { statuses.every( (status) => status === 'failure') ? (
                <div>
                    <p style={{ color: "red"}}>failed</p>
                    <button type='button' className='button' onClick={onClick} style={{marginBottom: '5px'}}>
                    <span className='button__text'>View Details</span>
                    <span className='button__icon'>
                    <ion-icon name="ellipsis-vertical-outline"></ion-icon>
                    </span>
                    
                    </button>

                    </div>
                ) : statuses.every( (status) => status === 'success') ? (
                    <div>
                        <p style={{color: "green"}}>success</p>
                            <button type='button' className='button' onClick={onClick} style={{marginBottom: '5px'}}>
                            <span className='button__text'>View Details</span>
                            <span className='button__icon'>
                            <ion-icon name="ellipsis-vertical-outline"></ion-icon>
                            </span>
                            </button>
                    </div>
                ) : <div>
                <p style={{color: "orange"}}>Manual Intervention Needed</p>
                    <button type='button' className='button' onClick={onClick} style={{marginBottom: '5px'}}>
                    <span className='button__text'>View Details</span>
                    <span className='button__icon'>
                    <ion-icon name="ellipsis-vertical-outline"></ion-icon>
                    </span>
                    </button>
            </div>
            }
        </div>
    )
}

export default UnsubscribeStatuses