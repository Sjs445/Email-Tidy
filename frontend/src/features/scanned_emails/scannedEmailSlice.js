import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import scannedEmailService from './scannedEmailService';

const initialState = {
    scanned_emails: [],
    scan_task_id: null,
    unsubscribe_task_id: null,
    task_status: {},
    progress: {},
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

// Get the scanned email task status by task id
export const getTaskStatus = createAsyncThunk('scanned_emails/getTaskStatus', async (task_id, thunkAPI) => {
    try {
        const token = thunkAPI.getState().auth.user;

        // If there's no token reject early
        if ( !token ) {
            return thunkAPI.rejectWithValue("Unauthorized");
        }

        return await scannedEmailService.getTaskStatus(task_id, token);

    } catch (error) {
        const message = (error.response && error.response.data && error.response.data.message) || error.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

// Unsubscribe from all emails
export const unsubscribeFromAll = createAsyncThunk('scanned_emails/unsubscribeFromAll', async( unsubscribeData, thunkAPI ) => {
    try {
        const token = thunkAPI.getState().auth.user;

        // If there's no token reject early.
        if( !token ) {
            return thunkAPI.rejectWithValue("Unauthorized");
        }

        return await scannedEmailService.unsubscribeFromAll(unsubscribeData, token);
    } catch ( error ) {
        const message = (error.response && error.response.data && error.response.data.detail) || error.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

// Update the task_status based on the state
export const updateTaskStatus = createAsyncThunk('scanned_emails/updateTaskStatus', async (_, thunkAPI) => {
    try {
        const task_status = thunkAPI.getState().scanned_email.task_status;
        const progress = thunkAPI.getState().scanned_email.progress;

        if ( task_status.state === 'PROGRESS') {
            const total = task_status.details.total;
            const current = task_status.details.current;
            const percent = (current/total) * 100;

            // Round to the nearest tenth
            const rounded = +(Math.round(percent + "e+2")  + "e-2");
            return { filled: rounded }
        }
        else if ( task_status.state === 'FAILURE' ) {
            throw "An error occurred while scanning your inbox";
        }
        else if ( task_status.state === 'SUCCESS' ) {
            return { filled: 100 };
        }
        else {
            const wait_attempts = progress.wait_attempts ? progress.wait_attempts + 1 : 1;
            return { filled: 0, wait_attempts: wait_attempts };
        }
    } catch (error) {
        return thunkAPI.rejectWithValue(error);
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
            state.scan_task_id = action.payload
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
        .addCase(unsubscribeFromAll.pending, (state) => {
            state.isLoading = true
        })
        .addCase(unsubscribeFromAll.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.unsubscribe_task_id = action.payload
        })
        .addCase(unsubscribeFromAll.rejected, (state, action) => {
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
            state.scan_task_id = action.payload.scan_task_id
            state.unsubscribe_task_id = action.payload.unsubscribe_task_id
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
        .addCase(getTaskStatus.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.task_status = action.payload
        })
        .addCase(getTaskStatus.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
        })
        .addCase(updateTaskStatus.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.progress = action.payload
        })
        .addCase(updateTaskStatus.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
        })
    }
});

export const { reset } = scannedEmailSlice.actions
export default scannedEmailSlice.reducer
