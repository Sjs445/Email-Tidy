import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import scannedEmailService from './scannedEmailService';

const initialState = {
    scanned_emails: [],
    task_id: null,
    scanned_email_count: 0,
    isError: false,
    isSuccess: false,
    isLoading: false,
    message: ''
}

// Scan a linked email
export const scanLinkedEmail = createAsyncThunk('scanned_emails/scan', async(scannedEmailData, thunkAPI) => {
    try {
        const token = thunkAPI.getState().auth.user;
        return await scannedEmailService.scanLinkedEmail(scannedEmailData, token);
    } catch (error) {
        const message = (error.response && error.response.data && error.response.data.detail) || error.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

// Get scanned email data for a linked email address
export const getScannedEmails = createAsyncThunk('scanned_emails/get', async( getScannedEmailData, thunkAPI) => {
    try {
        const token = thunkAPI.getState().auth.user;
        return await scannedEmailService.getScannedEmails(getScannedEmailData, token);
    } catch (error) {
        const message = (error.response && error.response.data && error.response.data.message) || error.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

// Unsubscribe from links
export const unsubscribeFromLinks = createAsyncThunk('scanned_emails/unsubscribe', async(unsubscribeData, thunkAPI) => {
    try {
        const token = thunkAPI.getState().auth.user;
        return await scannedEmailService.unsubscribeFromLinks(unsubscribeData, token);
    } catch (error) {
        const message = (error.response && error.response.data && error.response.data.message) || error.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

// Check to see if there's a running task for this linked email
export const getRunningTask = createAsyncThunk('scanned_emails/getRunningTask', async (linked_email, thunkAPI) => {
    try {
        const token = thunkAPI.getState().auth.user;

        // If there's no token reject early
        if ( !token ) {
            return thunkAPI.rejectWithValue("Unauthorized");
        }

        return await scannedEmailService.getRunningTask(linked_email, token);

    } catch (error) {
        const message = (error.response && error.response.data && error.response.data.message) || error.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

// Check to see if there's a running task for this linked email
export const getScannedEmailCount = createAsyncThunk('scanned_emails/getScannedEmailCount', async (linked_email, thunkAPI) => {
    try {
        const token = thunkAPI.getState().auth.user;

        // If there's no token reject early
        if ( !token ) {
            return thunkAPI.rejectWithValue("Unauthorized");
        }

        return await scannedEmailService.getScannedEmailCount(linked_email, token);

    } catch (error) {
        const message = (error.response && error.response.data && error.response.data.message) || error.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const scannedEmailSlice = createSlice({
    name: 'scanned_email',
    initialState,
    reducers: {
        reset: (state) => initialState
    },
    extraReducers: (builder) => {
        builder
         .addCase(scanLinkedEmail.pending, (state) => {
            state.isLoading = true
         })
         .addCase(scanLinkedEmail.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.task_id = action.payload
         })
         .addCase(scanLinkedEmail.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
         })
         .addCase(getScannedEmails.pending, (state) => {
            state.isLoading = true
        })
        .addCase(getScannedEmails.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.scanned_emails = action.payload
        })
        .addCase(getScannedEmails.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
        })
        .addCase(unsubscribeFromLinks.pending, (state) => {
            state.isLoading = true
        })
        .addCase(unsubscribeFromLinks.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.scanned_emails = action.payload
        })
        .addCase(unsubscribeFromLinks.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
        })
        .addCase(getRunningTask.pending, (state) => {
            state.isLoading = true
        })
        .addCase(getRunningTask.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.task_id = action.payload
        })
        .addCase(getRunningTask.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
        })
        .addCase(getScannedEmailCount.pending, (state) => {
            state.isLoading = true
        })
        .addCase(getScannedEmailCount.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.scanned_email_count = action.payload
        })
        .addCase(getScannedEmailCount.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
        })
    }
});

export const { reset } = scannedEmailSlice.actions
export default scannedEmailSlice.reducer
