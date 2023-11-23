import {
    createSlice,
    PayloadAction,
    createAsyncThunk,
    createSelector,
} from "@reduxjs/toolkit"
import axios from "axios"
import { RootState } from "../../redux/store"

interface UserState {
    id: string | null
    token: string | null
    name: string | null
    email: string | null
    isLoggedIn: boolean
    registrationState: 'in-progress'|'success'|'failure'|null,
}

const initialState: UserState = {
    id: null,
    token: null,
    name: null,
    email: null,
    isLoggedIn: false,
    registrationState: null,
}

const userSlice = createSlice({
    name: "user",
    initialState,
    reducers: {
        resetRegistrationState(state) {
            state.registrationState = null
        },
        logout(state) {
            state.id = null
            state.name = null
            state.email = null
            state.isLoggedIn = false
        },
    },
    extraReducers: (builder) => {
        builder.addCase(loginUser.fulfilled, (state, action) => {
            const { user, token } = action.payload;
            state.id = user.id;
            state.name = user.username;
            state.email = user.email;
            state.isLoggedIn = true;
            state.token = token;
        });
        builder.addCase(loginUser.rejected, (state, action) => {
            console.error('Login failed:', action.payload);
        });
        builder.addCase(signinUser.pending, (state, action) => {
            state.registrationState = 'in-progress';
        });
        builder.addCase(signinUser.fulfilled, (state, action) => {
            state.registrationState = 'success';
            ;
        });
        builder.addCase(signinUser.rejected, (state, action) => {
            state.registrationState = 'failure';
            console.error('Registration failed:', action.error);
        });
    },
})

// Selectors
export const selectUser = (state: RootState) => state.user

export const selectUserName = createSelector([selectUser], (user) => user.name)
export const selectRegistrationState = createSelector([selectUser], (user) => user.registrationState)

// Thunks
export const loginUser = createAsyncThunk(
    "user/login",
    async (credentials: { email: string; password: string }, thunkAPI) => {
        try {
            const response = await axios.post(
                "http://localhost:8080/users/login",
                credentials
            )
            return response.data
        } catch (error) {
            if (axios.isAxiosError(error) && error.response) {
                return thunkAPI.rejectWithValue(error.response.data)
            }
            return thunkAPI.rejectWithValue((error as Error).message)
        }
    }
)

export const signinUser = createAsyncThunk(
    "user/signin",
    async (user: { username: string ,email: string; password: string }, thunkAPI) => {
        try {
            const response = await axios.post(
                "http://localhost:8080/users/register",
                user
            )
            return response.data
        } catch (error) {
            if (axios.isAxiosError(error) && error.response) {
                return thunkAPI.rejectWithValue(error.response.data)
            }
            return thunkAPI.rejectWithValue((error as Error).message)
        }
    }
)

export const { logout, resetRegistrationState } = userSlice.actions

export default userSlice.reducer
