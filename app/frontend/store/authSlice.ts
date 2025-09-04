import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import axios from 'axios';
import i18next from 'i18next';

// Типы для данных авторизации
interface AuthData {
  token: string;
  username: string;
}

interface AuthState {
  username: string | null;
  token: string | null;
  isAuthorized: boolean;
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}

// Начальное состояние с типом
const initialState: AuthState = {
  username: localStorage.getItem('username') || null,
  token: localStorage.getItem('token') || null,
  isAuthorized: !!localStorage.getItem('token'),
  status: 'idle',
  error: null,
};

export const getIsAuthorized = (state: { auth: AuthState }) => state.auth.isAuthorized;
export const getUsername = (state: { auth: AuthState }) => state.auth.username;
export const getToken = (state: { auth: AuthState }) => state.auth.token;
export const getAuthError = (state: { auth: AuthState }) => state.auth.error;
export const getAuthStatus = (state: { auth: AuthState }) => state.auth.status;

export const login = createAsyncThunk<AuthData, { username: string; password: string }, { rejectValue: string }>(
  'auth/login',
  async (data, { rejectWithValue }) => {
    try {
      const response = await axios.post<AuthData>('/auth/login/', data);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || i18next.t('errors.authErr'));
    }
  }
);

export const signup = createAsyncThunk<AuthData, { username: string; password: string }, { rejectValue: string }>(
  'auth/signup',
  async ({ username, password }, { rejectWithValue }) => {
    try {
      const response = await axios.post<AuthData>('/auth/register/', { username, password });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || i18next.t('errors.signupErr'));
    }
  }
);


const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setAuthorized(state, action: PayloadAction<boolean>) {
      state.isAuthorized = action.payload;
    },
    clearAuthError(state) {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action: PayloadAction<AuthData>) => {
        localStorage.setItem('token', action.payload.token);
        localStorage.setItem('username', action.payload.username);
        state.status = 'succeeded';
        state.token = action.payload.token;
        state.username = action.payload.username;
        state.isAuthorized = true;
      })
      .addCase(login.rejected, (state, action: PayloadAction<string | undefined>) => {
        state.status = 'failed';
        state.error = action.payload || 'Unknown error';
      })
      .addCase(signup.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(signup.fulfilled, (state, action: PayloadAction<AuthData>) => {
        localStorage.setItem('token', action.payload.token);
        localStorage.setItem('username', action.payload.username);
        state.status = 'succeeded';
        state.token = action.payload.token;
        state.username = action.payload.username;
        state.isAuthorized = true;
      })
      .addCase(signup.rejected, (state, action: PayloadAction<string | undefined>) => {
        state.status = 'failed';
        state.error = action.payload || 'Unknown error';
      });
  },
});


export type { AuthState, AuthData };
export const { setAuthorized, clearAuthError } = authSlice.actions;
export default authSlice.reducer;