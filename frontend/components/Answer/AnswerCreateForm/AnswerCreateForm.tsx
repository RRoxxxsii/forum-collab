'use client'
import { TiptapEditor } from '@/components/TiptapEditor'
import { UploadImage } from '@/components/UploadImage'
import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { BASE_URL } from '@/shared/constants'
import { IAnswer, IErrorRes, IQuestion, IUser } from '@/types'
import { Button, Typography } from '@mui/material'
import { getCookie } from 'cookies-next'
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
	let formField = new FormData()

	if (questionData) {
		formField.append('question', questionData?.id.toString())
	}
	if (answerContent) {
		formField.append('answer', answerContent)
	}
	if (answerImages) {
		answerImages?.forEach((image) => {
			formField.append('uploaded_images', image)
		})
	}

	console.log(formField)

	const access_token = getCookie('access_token')

	try {
		const response = await fetch(`${BASE_URL}/forum/answer-question/`, {
			method: 'POST',
			headers: {
				Authorization: `${access_token ? `Bearer ${access_token}` : ''}`,
			},
			body: formField,
		})

		const data: IAnswer | IErrorRes = await response.json()

		if ('error' in data) {
			throw new Error(data.error)
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
	} catch (error) {
		if (error instanceof Error) {
			toast.error(error.message, {
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
	}
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
			<input
				type='file'
				accept='image/*' // only accept image file types
				multiple // allow multiple images
				onChange={(e) => {
					// this gives us the data on what files are selected
					// however, it's of type `FileList` which is hard to modify.
					const fileList = e.target.files
					// let's convert `FileList` into a `File[]`
					if (fileList) {
						const files = [...fileList] // now we have `File[]` type
						// This only works on es6 version make sure to set your tsconfig.json "target" to "es6"
						setAnswerImages(files)
					}
				}}
				className='bg-gray-100'
			/>
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
