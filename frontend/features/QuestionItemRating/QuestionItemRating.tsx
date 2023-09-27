'use client'
import { IQuestion } from '@/types/types'
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward'
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward'
import { Box, IconButton, Typography } from '@mui/material'

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
			}}>
			<IconButton onClick={() => setLike({ id: questionData.id })}>
				<ArrowUpwardIcon></ArrowUpwardIcon>
			</IconButton>
			<Typography fontWeight={700}>
				{questionData.rating?.like_amount - questionData.rating?.dislike_amount}
			</Typography>
			<IconButton onClick={() => setDislike({ id: questionData.id })}>
				<ArrowDownwardIcon></ArrowDownwardIcon>
			</IconButton>
		</Box>
	)
}
