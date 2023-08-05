import axios from "axios";

const API_URL = '/scanned_emails/';

// Scan a linked email for spam
const scanLinkedEmail = async ( scanEmailData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.post(API_URL, scanEmailData, config);

    return response.data;
}

// Get a list of scanned emails for a linked email
const getScannedEmails = async ( getScannedEmailData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    let url = API_URL;

    // Add optional params
    url += ( "undefined" !== typeof(getScannedEmailData.page) ? getScannedEmailData.page : '' );
    url += ( getScannedEmailData.linked_email ? `?linked_email=${getScannedEmailData.linked_email}` : '' );
    url += ( getScannedEmailData.emailFrom ? `?email_from=${getScannedEmailData.emailFrom}` : '');

    const response = await axios.get(url, config);

    return response.data;
}

const scannedEmailService = {
    scanLinkedEmail,
    getScannedEmails,
}

export default scannedEmailService
