'use client'
import { Transliterate } from '@/shared/transliterate'
import { ICustomFile, IErrorRes, IQuestion, ITag } from '@/types'
import { Button } from '@mui/material'
import { useRouter } from 'next/navigation'
import { toast } from 'react-toastify'

interface SubmitResponse {
	content: string
	question: number
	title: string
	user: string
	tags?: ITag[]
	error?: any
}

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
	images: File[]
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

			const result: SubmitResponse = await response.json()

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
			router.push(
				`/question/${result?.question}/${Transliterate(
					result?.title
				)}?tags=${result?.tags?.map((tag) => Transliterate(tag.tag_name))}`
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

			const result: IQuestion | IErrorRes = await response.json()

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
				render: 'Вопрос изменён',
				type: 'success',
				isLoading: false,
				autoClose: 3000,
			})
			router.push(
				`/question/${result?.id}/${Transliterate(
					result?.title
				)}?tags=${result?.tags?.map((tag) => Transliterate(tag.tag_name))}`
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
