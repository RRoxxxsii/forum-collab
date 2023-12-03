import { toast } from 'react-toastify'

export const handleSolve = async ({ answerId }: { answerId: number }) => {
	const solveToast = toast.loading('Обработка ответа...')
	try {
		const response = await fetch('/api/forum/mark-answer-solving', {
			method: 'POST',
			body: JSON.stringify({
				question_answer_id: answerId,
			}),
			headers: { 'Content-Type': 'application/json' },
		})

		const result = await response.json()

		if (!response.ok) {
			throw new Error(result.error.detail)
		}

		toast.update(solveToast, {
			render: result.message,
			type: 'success',
			isLoading: false,
			autoClose: 3000,
		})
	} catch (error) {
		toast.update(solveToast, {
			render: typeof error === 'string' ? error : (error as Error).message,
			type: 'error',
			isLoading: false,
			autoClose: 3000,
		})
	}
}
