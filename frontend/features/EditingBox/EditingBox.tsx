import { IAnswer } from '@/types'
import { TiptapEditor } from '@/widgets/TiptapEditor'
import { Box } from '@mui/material'
import { Dispatch, SetStateAction, useEffect, useRef, useState } from 'react'
import { AskAnswerFormSubmit } from '../AskAnswerFormSubmit'

export const EditingBox = ({
	isEditing,
	setIsEditing,
	answerData,
}: {
	isEditing: boolean
	setIsEditing: Dispatch<SetStateAction<boolean>>
	answerData: IAnswer
}) => {
	const [newContent, setNewContent] = useState<string>(answerData.answer)

	const editingBoxRef = useRef<HTMLDivElement | null>(null)
	const handleClickOutside = (event: MouseEvent) => {
		if (
			editingBoxRef.current &&
			!editingBoxRef.current.contains(event.target as Node)
		) {
			// setIsEditing(false)
		}
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
				answerContent={answerData.answer}
				questionId={answerData.question}
				images={[]}
				setIsEditing={setIsEditing}
			/>
		</Box>
	)
}
