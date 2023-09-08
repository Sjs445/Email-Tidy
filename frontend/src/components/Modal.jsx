function Modal({open, onClose}) {
    if (!open) return null;
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
              <p>Link 1</p>
            </div>
          </div>
        </div>
      </div>
    );
}

export default Modal