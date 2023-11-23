import * as React from "react"
import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField"
import Dialog from "@mui/material/Dialog"
import DialogActions from "@mui/material/DialogActions"
import DialogContent from "@mui/material/DialogContent"
import Tabs from "@mui/material/Tabs"
import Tab from "@mui/material/Tab"
import { Box, Alert } from "@mui/material"
import { SxProps } from "@mui/material"
import { useAppDispatch, useAppSelector } from "../../redux/hooks"
import { selectRegistrationState, loginUser, signinUser, resetRegistrationState } from "./userSlice"

//#region interfaces
interface LoginDialogProps {
    open: boolean
    setOpen: React.Dispatch<React.SetStateAction<boolean>>
}
//#endregion

const LoginDialog = ({ open, setOpen }: LoginDialogProps) => {
    const [selectedTab, setSelectedTab] = React.useState(0)
    const [logInFormData, setLogInFormData] = React.useState({
        email: "",
        password: "",
    })
    const [signInFormData, setSignInFormData] = React.useState({
        username: "",
        email: "",
        password: "",
    })
    const dispatch = useAppDispatch()
    const registrationState = useAppSelector(selectRegistrationState)

    const handleLogInFormChanged = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault()
        const { name, value } = e.target
        setLogInFormData({ ...logInFormData, [name]: value })
    }

    const handleSignInFormChanged = (
        e: React.ChangeEvent<HTMLInputElement>
    ) => {
        e.preventDefault()
        const { name, value } = e.target
        setSignInFormData({ ...signInFormData, [name]: value })
    }

    const handleSwitchedTab = (
        event: React.SyntheticEvent,
        newValue: number
    ) => {
        console.log(`Switching to tab ${newValue}`)
        event.preventDefault()
        setSelectedTab(newValue)
    }

    const handleClose = () => {
        setOpen(false)
    }

    const handleCreateAccount = () => {
        dispatch(
            signinUser({
                username: signInFormData.username,
                email: signInFormData.email,
                password: signInFormData.password,
            })
        )
    }

    const handleConnect = () => {
        dispatch(
            loginUser({
                email: logInFormData.email,
                password: logInFormData.password,
            })
        )
        setOpen(false)
    }

    interface TabChildProps {
        children?: React.ReactNode
        index: number
        value: number
        sx?: SxProps
    }

    function CustomTabPanel(props: TabChildProps) {
        const { children, value, index, ...other } = props

        return (
            <Box role="tabpanel" hidden={value !== index} {...other}>
                {children}
            </Box>
        )
    }

    const RegistrationAlert = (state: string|null) => {
        switch (state) {
            case "failure": {
                return (
                    <Alert severity="error">
                        Registration failed, check your inputs.{" "}
                    </Alert>
                )
            }
            case "success": {
                return (
                    <Alert severity="success">
                        Registration successful ! You can now log-in.
                    </Alert>
                )
            }
            case "in-progress": {
                return (
                    <Alert severity="info">Registration in progress...</Alert>
                )
            }
            default:
                break
        }
    }

    React.useEffect(() => {
        if (!open) {
            dispatch(resetRegistrationState())
            setSignInFormData({
                username: "",
                email: "",
                password: "",
            })
        }
    },[open])

    return (
        <div>
            <Dialog open={open} onClose={handleClose}>
                {/* <DialogTitle>Subscribe</DialogTitle> */}
                <DialogContent>
                    <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
                        <Tabs
                            value={selectedTab}
                            onChange={handleSwitchedTab}
                            aria-label="basic tabs example"
                        >
                            <Tab key="login-tab" label="Log-in" />
                            <Tab key="signin-tab" label="Create account" />
                        </Tabs>
                        <Box
                            role="tabpanel"
                            hidden={selectedTab !== 0}
                            key="login-panel"
                            sx={{ p: 3 }}
                        >
                            <TextField
                                // autoFocus
                                margin="dense"
                                key="email"
                                name="email"
                                label="Email Address"
                                value={logInFormData.email}
                                onChange={handleLogInFormChanged}
                                type="email"
                                fullWidth
                                variant="standard"
                            />
                            <TextField
                                // autoFocus
                                margin="dense"
                                key="password"
                                name="password"
                                label="Password"
                                value={logInFormData.password}
                                onChange={handleLogInFormChanged}
                                type="password"
                                fullWidth
                                variant="standard"
                            />
                        </Box>
                        <Box
                            role="tabpanel"
                            hidden={selectedTab !== 1}
                            key="signin-panel"
                            sx={{ p: 3 }}
                        >
                            {RegistrationAlert(registrationState)}
                            <TextField
                                // autoFocus
                                margin="dense"
                                key="name"
                                name="username"
                                label="Username"
                                value={signInFormData.username}
                                onChange={handleSignInFormChanged}
                                fullWidth
                                variant="standard"
                            />
                            <TextField
                                // autoFocus
                                margin="dense"
                                key="email"
                                name="email"
                                label="Email Address"
                                value={signInFormData.email}
                                onChange={handleSignInFormChanged}
                                type="email"
                                fullWidth
                                variant="standard"
                            />
                            <TextField
                                // autoFocus
                                margin="dense"
                                key="password"
                                name="password"
                                label="Password"
                                value={signInFormData.password}
                                onChange={handleSignInFormChanged}
                                type="password"
                                fullWidth
                                variant="standard"
                            />
                        </Box>
                    </Box>
                </DialogContent>
                <DialogActions>
                    <CustomTabPanel
                        key="connect-panel"
                        value={selectedTab}
                        index={0}
                    >
                        <Button onClick={handleConnect}>Connect</Button>
                    </CustomTabPanel>
                    <CustomTabPanel
                        key="create-account-panel"
                        value={selectedTab}
                        index={1}
                    >
                        <Button onClick={handleCreateAccount}>
                            Create account
                        </Button>
                    </CustomTabPanel>
                    <Button onClick={handleClose}>Cancel</Button>
                </DialogActions>
            </Dialog>
        </div>
    )
}

export default LoginDialog
