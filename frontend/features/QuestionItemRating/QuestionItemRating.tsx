'use client'
import { IQuestion, IUser } from '@/types/types'
import {
	ArrowDownward,
	ArrowDownwardOutlined,
	ArrowUpward,
	ArrowUpwardOutlined,
} from '@mui/icons-material'
import { Box, Checkbox, Typography } from '@mui/material'
import { useState } from 'react'

type Model = 'question' | 'answer'

export interface LikeFunctionProps {
	id: number
	model: Model
	checked?: boolean
}

interface QuestionItemRatingProps {
	questionData: IQuestion
	profileData: IUser | null
	model: Model
	setLike: ({ id, model }: LikeFunctionProps) => Promise<null | undefined>
	setDislike: ({ id, model }: LikeFunctionProps) => Promise<null | undefined>
}

export const QuestionItemRating = ({
	questionData,
	profileData,
	model,
	setLike,
	setDislike,
}: QuestionItemRatingProps) => {
	const [userLike, setUserLike] = useState(0)
	const [checked, setChecked] = useState<null | number>(null)

	const handleUserLike = ({ id, model, checked }: LikeFunctionProps) => {
		setLike({ id: id, model: model })
		if (checked) {
			setUserLike((userLike) => (userLike = 1))
			setChecked(0)
		} else {
			setUserLike((userLike) => (userLike = 0))
			setChecked(null)
		}
	}

	const handleUserDislike = ({ id, model, checked }: LikeFunctionProps) => {
		setLike({ id: id, model: model })
		if (checked) {
			setUserLike((userLike) => (userLike = -1))
			setChecked(1)
		} else {
			setUserLike((userLike) => (userLike = 0))
			setChecked(null)
		}
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
				disabled={questionData?.user?.id === profileData?.id}
				checked={checked === 0}
				icon={<ArrowUpwardOutlined />}
				checkedIcon={<ArrowUpward />}
				onChange={(e) =>
					handleUserLike({
						id: questionData.id,
						model: model,
						checked: e.target.checked,
					})
				}
			/>
			<Typography fontWeight={700}>
				{questionData.rating?.like_amount -
					questionData.rating?.dislike_amount +
					userLike}
			</Typography>
			<Checkbox
				disabled={questionData?.user?.id === profileData?.id}
				checked={checked === 1}
				icon={<ArrowDownwardOutlined />}
				checkedIcon={<ArrowDownward />}
				onChange={(e) =>
					handleUserDislike({
						id: questionData.id,
						model: model,
						checked: e.target.checked,
					})
				}
			/>
		</Box>
	)
}
