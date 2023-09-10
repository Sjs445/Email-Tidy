import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../features/auth/authSlice';
import linkedEmailReducer from '../features/linked_emails/linkedEmailSlice';
import scannedEmailReducer from '../features/scanned_emails/scannedEmailSlice';
import unsubscribeLinkReducer from '../features/unsubscribe_links/unsusbscribeLinkSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    email: linkedEmailReducer,
    scanned_email: scannedEmailReducer,
    unsubscribe_links: unsubscribeLinkReducer,
  },
});
