import { Box, Container, Stack, Paper } from '@mui/material'
import PublicDashboards from '../features/public_dashboards/PublicDashboards'
import NewsFeed from '../features/newsfeed/NewsFeed'

const Home = () => {
    return (
        <Stack
            direction={{ xs: 'column', md: 'row' }}
            spacing={{ xs: 2, md: 2 }}
            mt={5}
            divider={
                <div
                    style={{
                        width: 1,
                        height: '100%',
                        backgroundColor: 'black',
                    }}
                />
            }
        >
            <Box
                sx={{
                    bgcolor: 'GrayText',
                    height: '100vh',
                    width: { xs: 1, md: 1 },
                }}
            >
                <PublicDashboards />
            </Box>
            <Box
                sx={{
                    bgcolor: 'GrayText',
                    height: '100vh',
                    width: { xs: 1, md: 0.5 },
                }}
            >
                <NewsFeed />
            </Box>
        </Stack>
    )
}

export default Home
