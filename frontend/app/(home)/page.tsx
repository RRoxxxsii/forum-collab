import { EmailAlert } from '@/components/EmailAlert'
import { QuestionList } from '@/components/Question/QuestionList'
import { CategoryTabs } from '@/components/Question/QuestionList/models'
import { QuestionListAskFast } from '@/components/Question/QuestionListAskFast'
import { Box } from '@mui/material'

export default async function HomePage() {
	return (
		<>
			<Box sx={Home} className='flex min-h-screen items-start relative'>
				<CategoryTabs />
				<Box sx={HomeContainer}>
					<Box sx={desktopList}>
						<EmailAlert />
						<QuestionListAskFast />
						<QuestionList />
					</Box>
					<Box sx={mobileList}>
						<EmailAlert />
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
	mt: { md: 3, xs: 4 },
	ml: { md: 2, xs: 0 },
}
