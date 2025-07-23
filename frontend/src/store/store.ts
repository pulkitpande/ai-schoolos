import { configureStore } from '@reduxjs/toolkit';

// Create a simple store for now
export const store = configureStore({
  reducer: {
    // Add reducers here as needed
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 