// src/Navbar.tsx
import React, { useState } from "react"
import { AppBar, Toolbar, Typography, Button, Avatar, Stack } from "@mui/material"
import { useTheme } from "@mui/material/styles"
import IconButton from "@mui/material/IconButton"
import MenuIcon from "@mui/icons-material/Menu"
import LoginDialog from "../user/LoginDialog"
//#region Redux
import { useAppDispatch, useAppSelector } from "../../redux/hooks"
import { selectUserName, logout } from "../user/userSlice"
//#endregion

const Navbar: React.FC = () => {
    const theme = useTheme()
    const [open, setOpen] = useState(false)

    const userName = useAppSelector(selectUserName)
    const dispatch = useAppDispatch()

    const handleClickLogin = () => {
        setOpen(true)
    }

    const handleClickLogout = () => {
        dispatch(logout())
    }

    function stringToColor(string: string) {
        let hash = 0
        let i

        /* eslint-disable no-bitwise */
        for (i = 0; i < string.length; i += 1) {
            hash = string.charCodeAt(i) + ((hash << 5) - hash)
        }

        let color = "#"

        for (i = 0; i < 3; i += 1) {
            const value = (hash >> (i * 8)) & 0xff
            color += `00${value.toString(16)}`.slice(-2)
        }
        /* eslint-enable no-bitwise */

        return color
    }

    function stringAvatar(name: string) {
        return {
            sx: {
                bgcolor: stringToColor(name),
            },
            children: `${name.split(" ")[0][0].toUpperCase()}`,
        }
    }

    return (
        <AppBar position="static" color="default">
            <Toolbar variant="dense">
                <IconButton
                    size="large"
                    edge="start"
                    color="inherit"
                    aria-label="menu"
                    sx={{ mr: 2 }}
                >
                    <MenuIcon />
                </IconButton>
                <Typography
                    variant="h6"
                    color="textPrimary"
                    component="div"
                    sx={{ flexGrow: 1 }}
                >
                    CryptoViz
                </Typography>
                {userName == null ? (
                    <Button
                        variant="text"
                        color="primary"
                        onClick={handleClickLogin}
                    >
                        Log-in
                    </Button>
                ) : (
                    <Stack direction="row" spacing={2} alignItems={'center'}>
                        <Button
                        variant="text"
                        color="primary"
                        onClick={handleClickLogout}
                    >
                        Log-out
                    </Button>
                        {/* <Typography variant="body1" color="initial">{userName}</Typography> */}
                        <Avatar {...stringAvatar(userName)} />
                    </Stack>
                )}
                <LoginDialog open={open} setOpen={setOpen} />
            </Toolbar>
        </AppBar>
    )
}

export default Navbar
