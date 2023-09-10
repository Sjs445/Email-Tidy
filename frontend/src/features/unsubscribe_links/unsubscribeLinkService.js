import axios from "axios";

const API_URL = '/unsubscribe_links/';

// Get unsubscribe links by a scanned email id
const getUnsubscribeLinks = async ( unsubscribeLinksData, token ) => {
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    }

    let url = `${API_URL}unsubscribe_links_by_email/${unsubscribeLinksData.scanned_email_id}?linked_email=${unsubscribeLinksData.linked_email}`

    const response = await axios.get(url, config);

    return response.data;
}

const unsubscribeLinkService = {
    getUnsubscribeLinks,
}

export default unsubscribeLinkService;
