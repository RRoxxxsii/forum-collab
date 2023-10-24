import { IQuestion } from '@/types/types'
import { Box, Chip, Typography } from '@mui/material'
import { UserInformation } from '../UserInformation'
import { useSearchParams } from 'next/navigation'

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
