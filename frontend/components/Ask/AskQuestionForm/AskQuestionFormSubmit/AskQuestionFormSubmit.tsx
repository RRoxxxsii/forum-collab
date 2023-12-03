'use client'
import { BASE_URL } from '@/shared/constants'
import { Transliterate } from '@/shared/utils/Transliterate'
import { IErrorRes, IQuestion, ITag } from '@/types'
import { Button } from '@mui/material'
import { getCookie } from 'cookies-next'
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

interface AskQuestionFormSubmitProps {
	questionTitle: string
	questionContent: string
	questionTags: string[]
	questionImages: File[]
	questionId?: number | null
	userId?: number | null
	type: 'edit' | 'create'
}

export const AskQuestionFormSubmit = ({
	questionTitle,
	questionContent,
	questionTags,
	questionImages,
	questionId,
	userId,
	type,
}: AskQuestionFormSubmitProps) => {
	const router = useRouter()

	const access_token = getCookie('access_token')

	async function createSubmit() {
		const questionToast = toast.loading('Открытие вопроса...')

		let formField = new FormData()
		formField.append('title', questionTitle)
		formField.append('content', questionContent)
		questionTags?.forEach((tag) => {
			formField.append('tags', tag)
		})
		questionImages?.forEach((image) => {
			formField.append('uploaded_images', image)
		})

		try {
			const response = await fetch(`${BASE_URL}/forum/ask-question/`, {
				method: 'POST',
				headers: {
					Authorization: `${access_token ? `Bearer ${access_token}` : ''}`,
				},
				body: formField,
			})

			const result: SubmitResponse = await response.json()

			if (!response.ok || 'error' in result) {
				if ('error' in result) {
					return toast.update(questionToast, {
						render: result.error.detail ?? result.error,
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
					title: questionTitle,
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
