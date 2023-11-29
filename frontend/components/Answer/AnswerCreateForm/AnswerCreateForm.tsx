'use client'
import { TiptapEditor } from '@/components/TiptapEditor'
import { UploadImage } from '@/components/UploadImage'
import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { IAnswer, IErrorRes, IQuestion, IUser } from '@/types'
import { Button, Typography } from '@mui/material'
import { Dispatch, SetStateAction, useContext, useState } from 'react'
import { toast } from 'react-toastify'

async function addAnswer({
	questionData,
	setQuestionData,
	answerContent,
	setAnswerContent,
	userDetails,
	answerImages,
}: {
	questionData: IQuestion | null
	answerContent: string | null
	setAnswerContent: Dispatch<SetStateAction<string>>
	setQuestionData: Dispatch<SetStateAction<IQuestion | null>>
	userDetails: IUser | null
	answerImages?: File[]
}) {
	try {
		const response = await fetch(`/api/forum/create-answer`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				question_id: questionData?.id,
				answer_content: answerContent,
				answerImages: answerImages,
			}),
		})

		const data: IAnswer | IErrorRes = await response.json()

		if ('error' in data) {
			return toast.error(data.error, {
				position: 'bottom-center',
				autoClose: 3000,
				hideProgressBar: false,
				closeOnClick: true,
				pauseOnHover: true,
				draggable: true,
				progress: undefined,
				theme: 'dark',
			})
		}

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
	const [answerImages, setAnswerImages] = useState<File[]>([])
	const { userDetails } = useContext(UserDetailsContext)

	return (
		<>
			<UploadImage
				setImages={setAnswerImages}
				model='answer'
				images={answerImages}
			/>
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
			<Typography sx={{ color: '#919191', fontSize: 14, display: 'flex' }}>
				{[
					answerImages && (
						<Typography sx={{ mr: 1 }}>Прикрепленные изображения: </Typography>
					),
					answerImages.map((image) => (
						<Typography sx={{ mr: 0.5 }}>{image.name},</Typography>
					)),
				]}
			</Typography>
			<Button
				sx={{ mt: 1, mb: 3, width: 220, height: 50 }}
				variant='outlined'
				onClick={() =>
					addAnswer({
						questionData: questionData,
						answerContent: answerContent,
						setAnswerContent: setAnswerContent,
						setQuestionData: setQuestionData,
						userDetails: userDetails,
						answerImages: answerImages,
					})
				}>
				Ответить
			</Button>
		</>
	)
}
