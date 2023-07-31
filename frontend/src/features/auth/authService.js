import axios from 'axios';

// Register user
const register = async (userData) => {

    const response = await axios.post('/users/register', userData);
    
    if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
    }

    return response.data.access_token;
}

// Login user
const login = async (userData) => {

    // Send the login request as form data. Because OAuth2PasswordRequestForm requires it.
    const response = await axios.post('/login/access-token', {
            username: userData.username,
            password: userData.password,
        },
        {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }
    );

    if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
    }

    return response.data.access_token;
}

// Logout
const logout = () => {
    localStorage.removeItem('access_token');
}

// Test auth token
const test_token = async (token) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }
    const response = await axios.post('/login/test-token', {}, config);

    return response.data;
}

const authService = {
    register,
    logout,
    login,
    test_token,
}

export default authService
