import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import linkedEmailService from './linkedEmailService';

const initialState = {
    linked_emails: [],
    isError: false,
    isSuccess: false,
    isLoading: false,
    message: ''
}

// Create new linked email
export const createLinkedEmail = createAsyncThunk('linked_emails/create', async (linkedEmailData, thunkAPI) => {
    try {
        const token = thunkAPI.getState().auth.user;
        return await linkedEmailService.createLinkedEmail(linkedEmailData, token);
    } catch (error) {
        const message = (error.respose && error.response.data && error.response.data.message) || error.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

// Get user linked emails
export const getLinkedEmails = createAsyncThunk('linked_emails/getAll', async (_, thunkAPI) => {
    try {
        const token = thunkAPI.getState().auth.user;
        return await linkedEmailService.getLinkedEmails(token);
    } catch (error) {
        const message = (error.respose && error.response.data && error.response.data.message) || error.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

// Delete linked email
export const deleteLinkedEmail = createAsyncThunk('linked_emails/delete', async (id, thunkAPI) => {
    try {
        const token = thunkAPI.getState().auth.user;
        return await linkedEmailService.deleteLinkedEmail(id, token);
    } catch (error) {
        const message = (error.respose && error.response.data && error.response.data.message) || error.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const linkedEmailSlice = createSlice({
    name: 'email',
    initialState,
    reducers: {
        reset: (state) => initialState
    },
    extraReducers: (builder) => {
        builder
         .addCase(createLinkedEmail.pending, (state) => {
            state.isLoading = true
         })
         .addCase(createLinkedEmail.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.linked_emails.push(action.payload)
         })
         .addCase(createLinkedEmail.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
         })
        .addCase(getLinkedEmails.pending, (state) => {
            state.isLoading = true
        })
        .addCase(getLinkedEmails.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.linked_emails = action.payload
        })
        .addCase(getLinkedEmails.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
        })
        .addCase(deleteLinkedEmail.pending, (state) => {
            state.isLoading = true
        })
        .addCase(deleteLinkedEmail.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.linked_emails = state.linked_emails.filter( (email) => email.id !== action.payload.id )
        })
        .addCase(deleteLinkedEmail.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
        })
    }
});

export const { reset } = linkedEmailSlice.actions
export default linkedEmailSlice.reducer
