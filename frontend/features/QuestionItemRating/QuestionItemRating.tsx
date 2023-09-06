'use client'
import { IRating } from '@/types/types'
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward'
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward'
import { Box, IconButton, Typography } from '@mui/material'
import React, { EventHandler } from 'react'

export const QuestionItemRating = ({ rating }: { rating: IRating }) => {
	const setLike = (event: React.SyntheticEvent) => {
		event.preventDefault()
	}
	const setDislike = (event: React.SyntheticEvent) => {
		event.preventDefault()
	}

	return (
		<Box
			sx={{
				display: 'flex',
				flexDirection: 'column',
				alignItems: 'center',
				mr: 2,
			}}>
			<IconButton onClick={setLike}>
				<ArrowUpwardIcon></ArrowUpwardIcon>
			</IconButton>
			<Typography fontWeight={700}>
				{rating?.like_amount - rating?.dislike_amount}
			</Typography>
			<IconButton onClick={setDislike}>
				<ArrowDownwardIcon></ArrowDownwardIcon>
			</IconButton>
		</Box>
	)
}
