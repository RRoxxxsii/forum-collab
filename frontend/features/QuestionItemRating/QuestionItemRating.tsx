'use client'
import { IQuestion } from '@/types/types'
import {
	ArrowDownward,
	ArrowDownwardOutlined,
	ArrowUpward,
	ArrowUpwardOutlined,
} from '@mui/icons-material'
import { Box, Checkbox, Typography } from '@mui/material'

type Model = 'question' | 'answer'

interface FunctionProps {
	id: number
	model: Model
}

interface QuestionItemRatingProps {
	questionData: IQuestion
	model: Model
	setLike: ({ id, model }: FunctionProps) => Promise<null | undefined>
	setDislike: ({ id, model }: FunctionProps) => Promise<null | undefined>
}

export const QuestionItemRating = ({
	questionData,
	model,
	setLike,
	setDislike,
}: QuestionItemRatingProps) => {
	return (
		<Box
			sx={{
				display: 'flex',
				flexDirection: 'column',
				alignItems: 'center',
				color: 'white',
			}}>
			<Checkbox
				icon={<ArrowUpwardOutlined />}
				checkedIcon={<ArrowUpward />}
				onClick={() => setLike({ id: questionData.id, model: model })}
			/>
			<Typography fontWeight={700}>
				{questionData.rating?.like_amount - questionData.rating?.dislike_amount}
			</Typography>
			<Checkbox
				icon={<ArrowDownwardOutlined />}
				checkedIcon={<ArrowDownward />}
				onClick={() => setDislike({ id: questionData.id, model: model })}
			/>
		</Box>
	)
}
