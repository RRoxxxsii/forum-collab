import { AskWrapper } from '@/shared/AskWrapper'
import { AskQuestionForm } from '@/widgets/AskQuestionForm'
import { Box } from '@mui/material'

export default function AskPage() {
	return (
		<Box className='flex min-h-screen items-start max-h-80 relative'>
			<Box sx={{ px: 3, width: '100%' }}>
				<Box>
					<AskWrapper>
						<AskQuestionForm />
					</AskWrapper>
				</Box>
			</Box>
		</Box>
	)
}
