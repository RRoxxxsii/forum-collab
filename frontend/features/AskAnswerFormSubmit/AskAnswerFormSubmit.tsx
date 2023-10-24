'use client'
import { Transliterate } from '@/shared/transliterate'
import { ErrorRes, IAnswer } from '@/types/types'
import { Button } from '@mui/material'
import { useRouter } from 'next/navigation'
import { toast } from 'react-toastify'

export const AskAnswerFormSubmit = ({
	answerContent,
	images,
	userId,
	questionId,
}: {
	answerContent: string
	images: string[]
	userId?: number | null
	questionId?: number | null
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
			console.log(error)
			toast.update(questionToast, {
				render: 'Разорвана связь с сервером, проверьте подключение',
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
		}
	}

	return (
		<Button variant='outlined' onClick={editSubmit} sx={{ height: 50, mt: 1 }}>
			Обновить вопрос
		</Button>
	)
}
