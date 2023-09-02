'use client'
import { Button } from '@mui/material'
import { redirect, useRouter } from 'next/navigation'
import { toast } from 'react-toastify'

export const AskQuestionFormSubmit = ({
	titleValue,
	questionContent,
	tags,
	images,
}: {
	titleValue: string
	questionContent: string
	tags: string[]
	images: string[]
}) => {
	const router = useRouter()

	async function onSubmit() {
		const questionToast = toast.loading('Открытие вопроса...')
		try {
			const tokenValid = await fetch('/api/auth/refresh', { method: 'GET' })

			if (tokenValid.ok) {
				const response = await fetch('/api/forum/ask-question', {
					method: 'POST',
					body: JSON.stringify({
						tags: tags,
						title: titleValue,
						content: questionContent,
						uploaded_images: images,
					}),
					headers: { 'Content-Type': 'application/json' },
				})

				const result = await response.json()
				console.log(result.code)
				if (!response.ok) {
					if (result.code === 'token_not_valid') {
						await fetch('/api/auth/refresh', { method: 'GET' })
						onSubmit()
						return null
					}
					let errorMessage = ''
					if (result?.tags) {
						errorMessage += 'Теги: '
						result.tags.forEach((error: string) => {
							errorMessage += error + ' '
						})
					}
					if (result?.title) {
						errorMessage += '\nЗаголовок: '
						result.tags.forEach((error: string) => {
							errorMessage += error + ' '
						})
					}
					toast.update(questionToast, {
						render:
							errorMessage.length > 0
								? errorMessage
								: 'Разорвана связь с сервером, проверьте подключение',
						type: 'error',
						isLoading: false,
						autoClose: 3000,
					})
					return null
				}
				toast.update(questionToast, {
					render: result.message,
					type: 'success',
					isLoading: false,
					autoClose: 3000,
				})
				router.push(`/question/${result.id}`)
			}
		} catch (error: any | unknown) {
			toast.update(questionToast, {
				render: 'Разорвана связь с сервером, проверьте подключение',
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
		}
	}

	return (
		<Button onClick={onSubmit} variant='contained' sx={{ height: 50 }}>
			Открыть вопрос
		</Button>
	)
}
