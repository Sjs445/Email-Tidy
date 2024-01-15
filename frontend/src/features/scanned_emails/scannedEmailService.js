import axios from "axios";

const API_URL = '/emailtidy-py/scanned_emails/';

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

    const response = await axios.post(API_URL + "get_scanned_emails", getScannedEmailData, config);

    return response.data.scanned_emails;
}

// Unsubscribe from links
const unsubscribeFromLinks = async ( unsubscribeData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.post("/emailtidy-py/unsubscribe_links/", unsubscribeData, config);

    return response.data.success;
}

// Unsubscribe from ALL links
const unsubscribeFromAll = async ( unsubscribeData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.post("/emailtidy-py/unsubscribe_links/unsubscribe_from_all", unsubscribeData, config);

    return response.data.unsubscribe_task_id;
}

// Get a running task by linked email
const getRunningTask = async ( linked_email, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.get(`/emailtidy-py/linked_emails/tasks/${linked_email}`, config);

    return response.data;
}

// Get the status of a running task
const getTaskStatus = async ( task_id, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.get(`${API_URL}task_status/${task_id}`, config);

    return response.data;
}

// Get email sender data
const getEmailSenders = async ( emailSenderData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.get(`${API_URL}senders/${emailSenderData.page}?linked_email=${emailSenderData.linked_email}`, config);

    return response.data.senders;
}

// Unsubscribe from selected senders
const unsubscribeFromSenders = async ( unsubscribeData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    const response = await axios.post("/emailtidy-py/unsubscribe_links/unsubscribe_from_senders", unsubscribeData, config);

    return response.data.unsubscribe_task_id;
}

const scannedEmailService = {
    getEmailSenders,
    scanLinkedEmail,
    getScannedEmails,
    getTaskStatus,
    getRunningTask,
    unsubscribeFromLinks,
    unsubscribeFromAll,
    unsubscribeFromSenders,
}

export default scannedEmailService
