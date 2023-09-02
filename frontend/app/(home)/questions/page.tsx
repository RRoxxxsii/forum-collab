import { CategoryTabs } from '@/widgets/CategoryTabs'
import { QuestionList } from '@/widgets/QuestionList'
import { QuestionListAskFast } from '@/widgets/QuestionListAskFast'
import { Home } from '@mui/icons-material'
import { Box, Typography } from '@mui/material'

export default async function QuestionPage() {
	return (
		<>
			<Typography variant='h1' align='center'>
				!This page is under construction!
			</Typography>
			<Box sx={{ p: 3 }}>Поиск по тегам:</Box>
			<Box
				sx={questionPage}
				className='flex min-h-screen items-start max-h-80 relative'>
				<CategoryTabs />
				<Box sx={questionPageContainer}>
					<Box sx={desktopList}>
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
const questionPage = {
	display: 'flex',
	minHeight: 'screen',
	flexDirection: { md: 'row', xs: 'column' },
}
const questionPageContainer = {
	width: '100%',
	mt: { md: 0, xs: 0 },
	ml: { md: 4, xs: 0 },
}
