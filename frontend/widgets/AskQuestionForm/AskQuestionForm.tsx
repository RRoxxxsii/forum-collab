import { AskQuestionFormSubmit } from '@/features/AskQuestionFormSubmit'
import { AskQuestionFormTags } from '@/features/AskQuestionFormTags'
import { Box, TextField } from '@mui/material'
import { TiptapEditor } from '../TiptapEditor'

export const AskQuestionForm = () => {
	return (
		<>
			<TextField
				type='text'
				autoFocus
				autoComplete='off'
				fullWidth
				label='Тема вопроса'
				id='headline'
				sx={{ mb: 2 }}
			/>
			<TiptapEditor />
			<Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
				<AskQuestionFormTags />
				<AskQuestionFormSubmit />
			</Box>
		</>
	)
}
