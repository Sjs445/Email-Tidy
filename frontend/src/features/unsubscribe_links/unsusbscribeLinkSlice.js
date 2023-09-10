import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import unsubscribeLinkService from './unsubscribeLinkService';

const initialState = {
    unsubscribe_links: [],
    isError: false,
    isSuccess: false,
    isLoading: false,
    message: ''
}

// Get unsubscribe links by scanned email id
export const getUnsubscribeLinks = createAsyncThunk('unsubscribe_links/get', async ( unsubscribe_link_data, thunkAPI ) => {
    try {
        const token = thunkAPI.getState().auth.user;
        return await unsubscribeLinkService.getUnsubscribeLinks(unsubscribe_link_data, token);
    } catch (error) {
        const message = (error.response && error.response.data && error.response.data.message) || error.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
})

export const unsubscribeLinkSlice = createSlice({
    name: 'unsubscribe_links',
    initialState,
    reducers: {
        reset: (state) => initialState
    },
    extraReducers: (builder) => {
        builder
        .addCase(getUnsubscribeLinks.pending, (state) => {
            state.isLoading = true
        })
        .addCase(getUnsubscribeLinks.fulfilled, (state, action) => {
            state.isLoading = false
            state.isSuccess = true
            state.unsubscribe_links = action.payload
        })
        .addCase(getUnsubscribeLinks.rejected, (state, action) => {
            state.isLoading = false
            state.isError = true
            state.message = action.payload
        })
    }
});

export const { reset } = unsubscribeLinkSlice.actions
export default unsubscribeLinkSlice.reducer
