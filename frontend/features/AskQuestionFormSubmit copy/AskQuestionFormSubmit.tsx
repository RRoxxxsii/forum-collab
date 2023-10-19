'use client'
import { Transliterate } from '@/shared/transliterate'
import { Button } from '@mui/material'
import { useRouter } from 'next/navigation'
import { toast } from 'react-toastify'

export const AskQuestionFormSubmit = ({
	titleValue,
	questionContent,
	tags,
	images,
	type,
	userId,
	questionId,
}: {
	titleValue: string
	questionContent: string
	tags: string[]
	images: string[]
	type: 'edit' | 'create'
	userId?: number | null
	questionId?: number | null
}) => {
	const router = useRouter()

	async function createSubmit() {
		const questionToast = toast.loading('Открытие вопроса...')
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

			const result = await response.json()

			if (!response.ok) {
				let errorMessage = ''
				if (result?.code) {
					errorMessage +=
						'Ваша текущая сессия истекла, попробуйте перезагрузить страницу '
				}
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
			router.push(
				`/question/${result.question}/${result.title}?tags=${result.tags}`
			)
		} catch (error: any | unknown) {
			toast.update(questionToast, {
				render: 'Разорвана связь с сервером, проверьте подключение',
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
		}
	}

	async function editSubmit() {
		if (!questionId || !userId) return null
		const questionToast = toast.loading('Обновление вопроса...')
		try {
			const response = await fetch('/api/forum/update-question', {
				method: 'POST',
				body: JSON.stringify({
					user: userId,
					title: titleValue,
					content: questionContent,
					id: questionId,
				}),
				headers: { 'Content-Type': 'application/json' },
			})

			const result = await response.json()

			if (!response.ok) {
				let errorMessage = ''
				if (result?.code) {
					errorMessage +=
						'Ваша текущая сессия истекла, попробуйте перезагрузить страницу '
				}
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
			router.push(
				`/question/${result.id}/${Transliterate(
					result.title
				)}?tags=${Transliterate(result.tags)}`
			)
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
		<Button
			onClick={type === 'create' ? createSubmit : editSubmit}
			sx={{ height: 50 }}>
			{type === 'create' ? 'Открыть вопрос' : 'Обновить вопрос'}
		</Button>
	)
}
