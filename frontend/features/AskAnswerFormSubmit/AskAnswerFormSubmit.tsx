'use client'
import { ErrorRes, IAnswer } from '@/types'
import { Button } from '@mui/material'
import { Dispatch, SetStateAction } from 'react'
import { toast } from 'react-toastify'

export const AskAnswerFormSubmit = ({
	answerContent,
	images,
	userId,
	questionId,
	setIsEditing,
}: {
	answerContent: string
	images: string[]
	userId?: number | null
	questionId?: number | null
	setIsEditing: Dispatch<SetStateAction<boolean>>
}) => {
	async function editSubmit() {
		const questionToast = toast.loading('Открытие вопроса...')

		try {
			const response = await fetch('/api/forum/update-answer', {
				method: 'POST',
				body: JSON.stringify({
					question: questionId,
					answer: answerContent,
				}),
				headers: { 'Content-Type': 'application/json' },
			})

			const result: IAnswer | ErrorRes = await response.json()

			if (!response.ok || 'error' in result) {
				if ('error' in result) {
					return toast.update(questionToast, {
						render: result.error,
						type: 'error',
						isLoading: false,
						autoClose: 3000,
					})
				} else {
					return toast.update(questionToast, {
						render: 'Неизвестная ошибка',
						type: 'error',
						isLoading: false,
						autoClose: 3000,
					})
				}
			}
			toast.update(questionToast, {
				render: 'Вопрос создан',
				type: 'success',
				isLoading: false,
				autoClose: 3000,
			})
		} catch (error: any) {
			toast.update(questionToast, {
				render: 'Разорвана связь с сервером, проверьте подключение',
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
		}
	}

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
				onClick={() => setIsEditing(false)}
				sx={{ height: 50, mt: 1, background: '#2b2b2b', color: '#6e6e6e' }}>
				Отменить
			</Button>
		</>
	)
}
