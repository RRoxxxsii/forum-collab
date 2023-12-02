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
		/>
	))
}
