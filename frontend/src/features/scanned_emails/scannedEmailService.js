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

    return response.data.scanned_emails;
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

    return response.data.scanned_emails;
}

// Unsubscribe from links
const unsubscribeFromLinks = async ( unsubscribeData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.post("/unsubscribe_links/", unsubscribeData, config);

    return response.data.scanned_emails;
}

const scannedEmailService = {
    scanLinkedEmail,
    getScannedEmails,
    unsubscribeFromLinks,
}

export default scannedEmailService
