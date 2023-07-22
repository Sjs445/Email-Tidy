import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../features/auth/authSlice';
import linkedEmailReducer from '../features/linked_emails/linkedEmailSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    email: linkedEmailReducer,
  },
});
