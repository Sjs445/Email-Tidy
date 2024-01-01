import axios from "axios";

const API_URL = '/scanned_emails/';

// Scan a linked email for spam. Starts a running task and returns a task id.
const scanLinkedEmail = async ( scanEmailData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.post(API_URL, scanEmailData, config);

    return response.data.task_id;
}

// Get a list of scanned emails for a linked email
const getScannedEmails = async ( getScannedEmailData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    let url = API_URL;

    // Add params
    url += ( "undefined" !== typeof(getScannedEmailData.page) ? getScannedEmailData.page : '' );
    url += `?linked_email=${getScannedEmailData.linked_email}`;
    url += `&email_from=${getScannedEmailData.email_from}`;

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

// Unsubscribe from ALL links
const unsubscribeFromAll = async ( unsubscribeData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.post("/unsubscribe_links/unsubscribe_from_all", unsubscribeData, config);

    return response.data.unsubscribe_task_id;
}

// Get a running task by linked email
const getRunningTask = async ( linked_email, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.get(`/linked_emails/tasks/${linked_email}`, config);

    return response.data;
}

// Get a count of scanned emails
const getScannedEmailCount = async ( linked_email, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.get(`/scanned_emails/count/${linked_email}`, config);

    return response.data.count;
}

// Get the status of a running task
const getTaskStatus = async ( task_id, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.get(`/scanned_emails/task_status/${task_id}`, config);

    return response.data;
}

// Get email sender data
const getEmailSenders = async ( emailSenderData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.get(`/scanned_emails/senders/${emailSenderData.page}?linked_email=${emailSenderData.linked_email}`, config);

    return response.data.senders;
}

// Unsubscribe from selected senders
const unsubscribeFromSenders = async ( unsubscribeData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.post("/unsubscribe_links/unsubscribe_from_senders", unsubscribeData, config);

    return response.data.unsubscribe_task_id;
}

const scannedEmailService = {
    getEmailSenders,
    scanLinkedEmail,
    getScannedEmails,
    getScannedEmailCount,
    getTaskStatus,
    getRunningTask,
    unsubscribeFromLinks,
    unsubscribeFromAll,
    unsubscribeFromSenders,
}

export default scannedEmailService
