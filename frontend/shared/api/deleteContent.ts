import { Model } from '@/types/types'
import { toast } from 'react-toastify'

export async function DeleteContent({
	id,
	model,
	toastEnabled,
}: {
	id: number
	model: Model
	toastEnabled?: boolean
}) {
	if (!id) return null

	const ERROR_VIEWS: Record<Model, string> = {
		answer: 'ответ',
		comment: 'коммента',
		question: 'вопроса',
	}
	const RESPONSE_VIEWS: Record<Model, string> = {
		answer: 'Ответ',
		comment: 'Коммент',
		question: 'Вопрос',
	}

	const errorView = ERROR_VIEWS[model]
	const responseView = RESPONSE_VIEWS[model]
	const toastID = toast.loading(`Удаление ${errorView}...`)

	try {
		const response = await fetch('/api/forum/delete-content', {
			method: 'POST',
			body: JSON.stringify({
				id: id,
				model: model,
			}),
			headers: { 'Content-Type': 'application/json' },
		})

		const result = await response.json()

		if (!response.ok) {
			toast.update(toastID, {
				render: `${result.detail}`,
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
			return
		}

		toast.update(toastID, {
			render: `${responseView} удалён`,
			type: 'success',
			isLoading: false,
			autoClose: 3000,
		})
	} catch (error: any | unknown) {
		toast.update(toastID, {
			render: 'Ошибка подключения к серверу, попробуйте позже',
			type: 'error',
			isLoading: false,
			autoClose: 3000,
		})
	}
}
