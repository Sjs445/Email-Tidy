import { useState, useEffect, useReducer } from 'react';
import {useSelector, useDispatch} from 'react-redux';
import {useNavigate} from 'react-router-dom';
import {toast} from 'react-toastify';
import {FaUser} from 'react-icons/fa';
import { register, reset} from '../features/auth/authSlice';
import Spinner from '../components/Spinner';

function Register() {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        password2: '',
    });

    const { first_name, last_name, email, password, password2 } = formData;

    const navigate = useNavigate();
    const dispatch = useDispatch();

    const {user, isLoading, isError, isSuccess, message} = useSelector((state) => state.auth );

    useEffect( () => {
        if(isError) {
            toast.error(message);
        }

        if(isSuccess || user) {
            navigate('/');
        }

        dispatch(reset());
    }, [user, isError, isSuccess, message, navigate, dispatch])

    const onChange = (e) => {
        setFormData( (prevState) => ({
            ...prevState,
            [e.target.name]: e.target.value,
        }) )
    };

    const onSubmit = (e) => {
        e.preventDefault();

        if(password !== password2) {
            toast.error('Passwords do not match')
        } else {
            const userData = {
                first_name, last_name, email, password,
            }

            dispatch(register(userData));
        }
    }

    if(isLoading) {
        return <Spinner />
    }

  return <>
  <section className="heading">
    <h1>
        <FaUser />Register
    </h1>
    <p>Please create an account</p>
  </section>

  <section className='form'>
    <form onSubmit={onSubmit}>
        <div className='form-group'>
        <input type='text' className='form-control' id='first_name' name='first_name' value={first_name} placeholder='Enter your first name' onChange={onChange} />
        </div>
        <div className='form-group'>
        <input type='text' className='form-control' id='last_name' name='last_name' value={last_name} placeholder='Enter your last name' onChange={onChange} />
        </div>
        <div className='form-group'>
        <input type='text' className='form-control' id='email' name='email' value={email} placeholder='Enter your email' onChange={onChange} />
        </div>
        <div className='form-group'>
        <input type='text' className='form-control' id='password' name='password' value={password} placeholder='Enter your password' onChange={onChange} />
        </div>
        <div className='form-group'>
        <input type='text' className='form-control' id='password2' name='password2' value={password2} placeholder='Confirm your password' onChange={onChange} />
        </div>
        <div className="form-group">
            <button type='submit' className='btn btn-block'>
                Submit
            </button>
        </div>
        
    </form>
  </section>
  </>
}

export default Register