import { AskQuestionForm } from '@/widgets/AskQuestionForm'
import { AskTabs } from '@/widgets/AskTabs'
import { Box, Paper } from '@mui/material'

const askPageWrapper = {
	width: '100%',
	padding: { md: 3, xs: 0 },
}

export default async function AskPage() {
	return (
		<Box className='flex min-h-screen items-start max-h-80 relative'>
			<Box sx={askPageWrapper}>
				<Paper
					elevation={2}
					variant={'elevation'}
					sx={{
						p: 2,
						position: 'relative',
						width: 'clamp(300px, 100%, 1200px)',
						height: '100%',
						minHeight: '400px',
						alignItems: 'center',
					}}>
					<AskTabs />
					<AskQuestionForm />
				</Paper>
			</Box>
		</Box>
	)
}
