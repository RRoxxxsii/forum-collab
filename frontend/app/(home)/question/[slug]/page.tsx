'use client'
import { QuestionItemRating } from '@/features/QuestionItemRating'
import { Box, Paper } from '@mui/material'
import { useSearchParams } from 'next/navigation'

export default function QuestionPage() {
	const searchParams = useSearchParams()
	console.log(searchParams)
	return (
		<Box>
			<Paper>
				<QuestionItemRating />
			</Paper>
		</Box>
	)
}
