import { Box, Typography, Chip } from '@mui/material'
import React from 'react'
import { UserInformation } from '../UserInformation'
import { IQuestion } from '@/types/types'

export const QuestionContent = ({
	questionData,
}: {
	questionData: IQuestion
}) => {
	return (
		<Box sx={{ mb: 2, ml: 1 }}>
			<UserInformation questionData={questionData} />
			<Typography variant='h6'>{questionData?.title}</Typography>
			<Typography
				sx={{ mb: 2 }}
				variant='body1'
				dangerouslySetInnerHTML={{
					__html: questionData?.content ?? 'error',
				}}
			/>
			<Box>
				{questionData.tags.map((tag) => (
					<Chip key={tag.tag_name} sx={{ mr: 1 }} label={tag.tag_name} />
				))}
			</Box>
		</Box>
	)
}
