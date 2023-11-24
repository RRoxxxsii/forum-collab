import { QuestionSearch } from '@/components/Question/QuestionSearch'
import { QuestionList } from '@/components/Question/QuestionList'
import { QuestionListAskFast } from '@/components/Question/QuestionListAskFast'

import { Box } from '@mui/material'

export default async function QuestionPage() {
	return (
		<>
			<Box
				sx={questionPage}
				className='flex min-h-screen items-start max-h-80 relative'>
				<Box sx={questionPageContainer}>
					<Box sx={desktopList}>
						<QuestionSearch />
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
	mt: 12,
	display: 'flex',
	minHeight: 'screen',
	flexDirection: { md: 'row', xs: 'column' },
}
const questionPageContainer = {
	width: '100%',
	mt: { md: 0, xs: 0 },
	ml: { md: 4, xs: 0 },
}
