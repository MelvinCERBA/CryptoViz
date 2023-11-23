import { Container } from '@mui/material'
import { useTheme } from '@mui/material/styles'
import Navbar from './features/navbar/Navbar'
import Home from './pages/Home'
import { Provider } from 'react-redux'
import store from './redux/store'

function App(): JSX.Element {
    const theme = useTheme()
    return (
        <>
            <Provider store={store}>
                <Navbar />
                <Container disableGutters>
                    <Home />
                </Container>
            </Provider>
        </>
    )
}

export default App
