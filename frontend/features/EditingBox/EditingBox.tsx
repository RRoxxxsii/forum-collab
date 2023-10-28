import { IAnswer, IErrorRes } from '@/types'
import { TiptapEditor } from '@/widgets/TiptapEditor'
import { Box } from '@mui/material'
import { Dispatch, SetStateAction, useEffect, useRef } from 'react'
import { toast } from 'react-toastify'
import { AskAnswerFormSubmit } from '../AskAnswerFormSubmit'

export const EditingBox = ({
	isEditing,
	setIsEditing,
	answerData,
	newContent,
	setNewContent,
}: {
	isEditing: boolean
	setIsEditing: Dispatch<SetStateAction<boolean>>
	newContent: string
	setNewContent: Dispatch<SetStateAction<string>>
	answerData: IAnswer
}) => {
	const editingBoxRef = useRef<HTMLDivElement | null>(null)
	const handleClickOutside = (event: MouseEvent) => {
		if (
			editingBoxRef.current &&
			!editingBoxRef.current.contains(event.target as Node)
		) {
			// setIsEditing(false)
		}
	}

	async function handleSubmit() {
		const questionToast = toast.loading('Открытие вопроса...')

		try {
			const response = await fetch('/api/forum/update-answer', {
				method: 'POST',
				body: JSON.stringify({
					questionId: answerData.question,
					answerId: answerData.id,
					answerContent: newContent,
				}),
				headers: { 'Content-Type': 'application/json' },
			})

			const result: IAnswer | IErrorRes = await response.json()

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
				render: 'Вопрос обновлен',
				type: 'success',
				isLoading: false,
				autoClose: 3000,
			})
			setIsEditing(false)
		} catch (error: any) {
			toast.update(questionToast, {
				render: 'Разорвана связь с сервером, проверьте подключение',
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
		}
	}

	const handleCancel = () => {
		setIsEditing(false)
		setNewContent(answerData.answer)
	}

	useEffect(() => {
		if (isEditing) {
			document.addEventListener('click', handleClickOutside)
		} else {
			document.removeEventListener('click', handleClickOutside)
		}

		return () => {
			document.removeEventListener('click', handleClickOutside)
		}
	}, [isEditing])

	return (
		<Box ref={editingBoxRef}>
			<TiptapEditor
				setContent={setNewContent}
				content={newContent}
				contentOnEdit={newContent}
				type='answer'
			/>
			<AskAnswerFormSubmit
				editSubmit={handleSubmit}
				editCancel={handleCancel}
			/>
		</Box>
	)
}
