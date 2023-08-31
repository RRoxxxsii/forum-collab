import { AskWrapper } from '@/shared/AskWrapper'
import { AskQuestionForm } from '@/widgets/AskQuestionForm'
import { Box } from '@mui/material'
import { cookies } from 'next/headers'

const askPageWrapper = {
	width: '100%',
	padding: { md: 3, xs: 0 },
}

export default async function AskPage() {
	return (
		<Box className='flex min-h-screen items-start max-h-80 relative'>
			<Box sx={askPageWrapper}>
				<Box>
					<AskWrapper>
						<AskQuestionForm />
					</AskWrapper>
				</Box>
			</Box>
		</Box>
	)
}
