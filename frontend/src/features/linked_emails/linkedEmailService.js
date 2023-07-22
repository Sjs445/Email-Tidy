import axios from "axios";

const API_URL = '/linked_emails/';

// Create new linked email
const createLinkedEmail = async ( linkedEmailData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.post(API_URL, linkedEmailData, config);

    return response.data;
}

// Get all linked emails
const getLinkedEmails = async ( token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.get(API_URL, config);

    return response.data.linked_emails;
}

// Delete linked email
const deleteLinkedEmail = async ( emailId, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.delete(API_URL + emailId, config);

    return response.data;
}

const linkedEmailService = {
    createLinkedEmail,
    getLinkedEmails,
    deleteLinkedEmail,
}

export default linkedEmailService;
