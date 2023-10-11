'use client'
import { BASE_URL } from '@/shared/constants'
import { IAnswer, IQuestion, IUser } from '@/types/types'
import { TiptapEditor } from '@/widgets/TiptapEditor'
import { Button, Typography } from '@mui/material'
import { Dispatch, SetStateAction, useState } from 'react'

async function addAnswer({
	questionData,
	setQuestionData,
	answerContent,
	setAnswerContent,
}: {
	questionData: IQuestion | null
	answerContent: string | null
	setAnswerContent: Dispatch<SetStateAction<string>>
	setQuestionData: Dispatch<SetStateAction<IQuestion | null>>
}) {
	try {
		const response = await fetch(`${BASE_URL}/forum/answer-question/`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				question: questionData?.id,
				answer: answerContent,
			}),
		})
		if (!response.ok) {
			throw new Error(response.statusText)
		}
		const data: IAnswer = await response.json()
		setAnswerContent('')
		setQuestionData((questionData) => {
			if (questionData) {
				return {
					...questionData,
					answers: [...questionData.answers, data],
				}
			}
			return null
		})
	} catch (error) {}
}

export const AnswerCreateForm = ({
	profileData,
	questionData,
	setQuestionData,
}: {
	profileData: IUser | null
	questionData: IQuestion | null
	setQuestionData: Dispatch<SetStateAction<IQuestion | null>>
}) => {
	const [answerContent, setAnswerContent] = useState<string>('')
	console.log(answerContent)
	return (
		<>
			<Typography
				variant='caption'
				color={'GrayText'}
				sx={{ display: 'flex', alignItems: 'center' }}>
				Ответить на вопрос как,
				<Typography variant='caption' sx={{ ml: 1 }} color={'lightblue'}>
					{profileData?.user_name ?? 'Гость'}
				</Typography>
			</Typography>
			<TiptapEditor
				type='answer'
				content={answerContent}
				setContent={setAnswerContent}
			/>
			<Button
				sx={{ mt: 1, mb: 3, width: 220, height: 50 }}
				variant='outlined'
				onClick={() =>
					addAnswer({
						questionData: questionData,
						answerContent: answerContent,
						setAnswerContent: setAnswerContent,
						setQuestionData: setQuestionData,
					})
				}>
				Ответить
			</Button>
		</>
	)
}
