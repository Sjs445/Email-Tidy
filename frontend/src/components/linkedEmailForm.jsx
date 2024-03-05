import {useState} from 'react';
import { UseSelector, useDispatch } from 'react-redux';
import {useNavigate} from 'react-router-dom';
import {toast} from 'react-toastify';
import {createLinkedEmail} from '../features/linked_emails/linkedEmailSlice';

function LinkedEmailForm() {
    const [formData, setFormData ] = useState({
        email: '',
        password: '',
    });

    const { email, password } = formData;

    const navigate = useNavigate();
    const dispatch = useDispatch();

    const onChange = (e) => {
        setFormData( (prevState) => ({
            ...prevState,
            [e.target.name]: e.target.value,
        }) )
    };
 
  const onSubmit = e => {
    e.preventDefault();

    if ( !email ) {
      return toast.error("Email is required");
    }

    if ( !password ) {
      return toast.error("Third Party Password is required");
    }

    const linkedEmailData = { email, password };

    dispatch(createLinkedEmail(linkedEmailData));
  }
  
  return <section className='form'>
    <form onSubmit={onSubmit}>
        <div className='form-group'>
            <p>Don't know how to create a third party password for your email? For instructions click <a onClick={() => navigate('/help')} style={{textDecoration:'underline', cursor:'pointer'}}>here.</a></p>
            <label htmlFor='email'>Linked Email</label>
            <input 
              type='text'
              id='email'
              name='email'
              value={email}
              onChange={onChange}
            />
            <label htmlFor='password'>Third Party Password</label>
            <input 
              type='password'
              id='password'
              name='password'
              value={password}
              onChange={onChange}
            />
        </div>
        <div className='form-group'>
            <button className="btn btn-block" type='submit'>
                Link Email
            </button>
        </div>
    </form>
  </section>
}

export default LinkedEmailForm