'use client'
import { AnswerCard } from '@/components/Answer/AnswerCard'
import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { DeleteContent } from '@/shared/api/deleteContent'
import { IAnswer, IModelType, IQuestion } from '@/types'
import { Dispatch, SetStateAction, useContext } from 'react'
import { toast } from 'react-toastify'

export const AnswerList = ({
	questionData,
	setQuestionData,
}: {
	questionData: IQuestion
	setQuestionData: Dispatch<SetStateAction<IQuestion | null>>
}) => {
	const { userDetails } = useContext(UserDetailsContext)

	const handleSolve = async ({ answerId }: { answerId: number }) => {
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

	const handleDelete = ({ id, model }: { id: number; model: IModelType }) => {
		DeleteContent({
			id: id,
			model: model,
		})
		if (model === 'answer') {
			setQuestionData({
				...questionData,
				answers: questionData.answers.filter((answer) => answer.id !== id),
			})
		}
		if (model === 'comment') {
			//why updating nested data has to be that complicated :((((((((((((((((((((((()))))))))))))))))))))))
			const updatedQuestionData = {
				...questionData,
				answers: questionData.answers.map((answer) => {
					if (answer.comments) {
						return {
							...answer,
							comments: answer.comments.filter((comment) => comment.id !== id),
						}
					}
					return answer
				}),
			}
			setQuestionData(updatedQuestionData)
		}
	}
	const sortedAnswers = questionData.answers.sort((a, b) =>
		a.is_solving ? -1 : 1
	)

	return sortedAnswers.map((answer: IAnswer) => (
		<AnswerCard
			key={answer.id}
			solved={answer.is_solving}
			answerData={answer}
			questionData={questionData}
			userDetails={userDetails}
			setQuestionData={setQuestionData}
			handleSolve={handleSolve}
			handleDelete={handleDelete}
		/>
	))
}
