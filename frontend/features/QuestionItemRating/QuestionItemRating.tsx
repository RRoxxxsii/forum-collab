'use client'
import { IQuestion } from '@/types/types'
import {
	ArrowDownward,
	ArrowDownwardOutlined,
	ArrowUpward,
	ArrowUpwardOutlined,
} from '@mui/icons-material'
import { Box, Checkbox, IconButton, Typography } from '@mui/material'

interface QuestionItemRatingProps {
	questionData: IQuestion
	setLike: ({ id }: { id: number }) => Promise<null | undefined>
	setDislike: ({ id }: { id: number }) => Promise<null | undefined>
}

export const QuestionItemRating = ({
	questionData,
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
				onClick={() => setLike({ id: questionData.id })}
			/>
			<Typography fontWeight={700}>
				{questionData.rating?.like_amount - questionData.rating?.dislike_amount}
			</Typography>
			<Checkbox
				icon={<ArrowDownwardOutlined />}
				checkedIcon={<ArrowDownward />}
				onClick={() => setDislike({ id: questionData.id })}
			/>
		</Box>
	)
}
