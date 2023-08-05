import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import scannedEmailService from './scannedEmailService';

const initialState = {
    scanned_emails: [],
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
        const message = (error.response && error.response.data && error.response.data.message) || error.message || error.toString();
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
            state.scanned_emails.push(action.payload)
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
            state.linked_emails = action.payload
        })
        .addCase(getScannedEmails.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
        })
    }
});

export const { reset } = scannedEmailSlice.actions
export default scannedEmailSlice.reducer
