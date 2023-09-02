import { CategoryTabs } from '@/widgets/CategoryTabs'
import { QuestionList } from '@/widgets/QuestionList'
import { QuestionListAskFast } from '@/widgets/QuestionListAskFast'

import { Alert, AlertTitle, Box } from '@mui/material'

export default async function HomePage() {
	return (
		<>
		
			<Box
				sx={Home}
				className='flex min-h-screen items-start max-h-80 relative'>
				<CategoryTabs />
				<Box sx={HomeContainer}>
					<Box sx={desktopList}>
						<Alert variant='outlined' severity='warning' sx={{ mb: 2 }}>
							<AlertTitle>Подтвердите почту</AlertTitle>
							Эта надпись исчезнет, когда вы подтведите свою почту
						</Alert>
						<QuestionListAskFast />
						<QuestionList />
					</Box>
					<Box sx={mobileList}>
						<QuestionListAskFast />
						<QuestionList />
					</Box>
				</Box>
			</Box>
		</>
	)
}

const desktopList = {
	width: 'clamp(300px, 100%, 1200px)',
	display: { md: 'block', xs: 'none' },
}
const mobileList = {
	width: 'clamp(300px, 100%, 1200px)',
	display: { md: 'none', xs: 'block' },
}
const Home = {
	display: 'flex',
	minHeight: 'screen',
	flexDirection: { md: 'row', xs: 'column' },
}
const HomeContainer = {
	width: '100%',
	mt: { md: 0, xs: 0 },
	ml: { md: 4, xs: 0 },
}
