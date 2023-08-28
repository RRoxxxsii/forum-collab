'use client'
import { Button } from '@mui/material'
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
	async function validateQuestion() {
		if (
			titleValue.length !== 0 &&
			questionContent.length !== 0 &&
			tags.length > 0 &&
			tags.length < 6
		) {
			return true
		}
		return false
	}
	async function onSubmit() {
		const questionToast = toast.loading('Открытие вопроса...')
		if (!validateQuestion) {
			toast.update(questionToast, {
				render: 'Заполните все поля',
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
			return null
		}

		try {
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

			const result = await response?.json()
			if (!response.ok) {
				toast.update(questionToast, {
					render: result?.detail ?? 'Произошла ошибка',
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
		} catch (error: any | unknown) {
			toast.update(questionToast, {
				render: error.message,
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
