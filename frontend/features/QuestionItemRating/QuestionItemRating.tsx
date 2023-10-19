'use client'
import { IQuestion, IUser } from '@/types/types'
import {
	ArrowDownward,
	ArrowDownwardOutlined,
	ArrowUpward,
	ArrowUpwardOutlined,
} from '@mui/icons-material'
import { Box, Checkbox, Typography } from '@mui/material'
import { Dispatch, SetStateAction, useState } from 'react'

export type Model = 'question' | 'answer'

export interface ChangeRatingProps {
	id: number
	model: Model
	action: 'like' | 'dislike'
	checked?: boolean
}

interface QuestionItemRatingProps {
	questionData: IQuestion | null
	setQuestionData: Dispatch<SetStateAction<IQuestion | null>>
	profileData: IUser | null
	model: Model
	setRating: ({
		id,
		model,
		action,
	}: ChangeRatingProps) => Promise<null | undefined>
}

export const QuestionItemRating = ({
	questionData,
	setQuestionData,
	profileData,
	model,
	setRating,
}: QuestionItemRatingProps) => {
	const [checked, setChecked] = useState<null | number>(null)

	const handleRating = ({ id, model, action, checked }: ChangeRatingProps) => {
		setRating({ id: id, model: model, action: action })
		setQuestionData((prevData) => {
			if (prevData === null) {
				return prevData
			}

			const updatedRating = { ...prevData.rating }

			if (action === 'like') {
				updatedRating.is_liked = true
				updatedRating.is_disliked = false
				updatedRating.like_amount = checked
					? updatedRating.like_amount + 1
					: updatedRating.like_amount - 1
			} else if (action === 'dislike') {
				updatedRating.is_liked = false
				updatedRating.is_disliked = true
				updatedRating.dislike_amount = checked
					? updatedRating.dislike_amount + 1
					: updatedRating.dislike_amount - 1
			}

			return {
				...prevData,
				rating: updatedRating,
			}
		})
	}

	if (!questionData) {
		return
	}

	return (
		<Box
			sx={{
				display: 'flex',
				flexDirection: 'column',
				alignItems: 'center',
				color: 'white',
			}}>
			<Checkbox
				defaultChecked={questionData.rating.is_liked}
				disabled={questionData.user?.id === profileData?.id}
				checked={questionData.rating.is_liked}
				icon={<ArrowUpwardOutlined />}
				checkedIcon={<ArrowUpward />}
				onChange={(e) =>
					handleRating({
						id: questionData.id,
						model: model,
						action: 'like',
						checked: e.target.checked,
					})
				}
			/>
			<Typography fontWeight={700}>
				{questionData.rating?.like_amount - questionData.rating?.dislike_amount}
			</Typography>
			<Checkbox
				defaultChecked={questionData.rating.is_disliked}
				disabled={questionData.user?.id === profileData?.id}
				checked={checked === 1}
				icon={<ArrowDownwardOutlined />}
				checkedIcon={<ArrowDownward />}
				onChange={(e) =>
					handleRating({
						id: questionData.id,
						model: model,
						action: 'dislike',
						checked: e.target.checked,
					})
				}
			/>
		</Box>
	)
}
