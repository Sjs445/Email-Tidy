import axios from 'axios';

// Register user
const register = async (userData) => {

    const response = await axios.post('/users/register', userData);
    
    if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
    }

    return response.data;
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

    return response.data;
}

// Logout
const logout = () => {
    localStorage.removeItem('access_token');
}

const authService = {
    register,
    logout,
    login,
}

export default authService
