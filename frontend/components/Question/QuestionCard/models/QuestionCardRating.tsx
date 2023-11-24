'use client'
import { IChangeRating, IModelType, IQuestion, UserDetailsType } from '@/types'
import {
	ArrowDownward,
	ArrowDownwardOutlined,
	ArrowUpward,
	ArrowUpwardOutlined,
} from '@mui/icons-material'
import { Box, Checkbox, Typography } from '@mui/material'
import { useState } from 'react'

interface QuestionCardRatingProps {
	questionData: IQuestion | null
	handleRating: ({ model, id, action, checked }: IChangeRating) => void
	profileData: UserDetailsType
	model: IModelType
}

export const QuestionCardRating = ({
	questionData,
	handleRating,
	profileData,
	model,
}: QuestionCardRatingProps) => {
	const [clientRating, setClientRating] = useState(0)
	const [checked, setChecked] = useState<null | number>(null)

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
				disabled={questionData.user?.id === profileData?.id}
				checked={checked === 0}
				icon={<ArrowUpwardOutlined />}
				checkedIcon={<ArrowUpward />}
				onChange={(e) =>
					handleRating({
						id: questionData.id,
						model: model,
						action: 'like',
						checked: questionData.rating.is_liked,
					})
				}
			/>
			<Typography fontWeight={700}>
				{questionData.rating?.like_amount -
					questionData.rating?.dislike_amount +
					clientRating || 0}
			</Typography>
			<Checkbox
				disabled={questionData.user?.id === profileData?.id}
				checked={checked === 1}
				icon={<ArrowDownwardOutlined />}
				checkedIcon={<ArrowDownward />}
				onChange={(e) =>
					handleRating({
						id: questionData.id,
						model: model,
						action: 'dislike',
						checked: questionData.rating.is_disliked,
					})
				}
			/>
		</Box>
	)
}
