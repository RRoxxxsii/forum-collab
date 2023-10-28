'use client'
import { Button } from '@mui/material'

export const AskAnswerFormSubmit = ({
	editSubmit,
	editCancel,
}: {
	editSubmit: () => void
	editCancel: () => void
}) => {
	return (
		<>
			<Button
				variant='outlined'
				onClick={editSubmit}
				sx={{ height: 50, mt: 1, mr: 1 }}>
				Обновить вопрос
			</Button>
			<Button
				variant='text'
				onClick={editCancel}
				sx={{ height: 50, mt: 1, background: '#2b2b2b', color: '#6e6e6e' }}>
				Отменить
			</Button>
		</>
	)
}
