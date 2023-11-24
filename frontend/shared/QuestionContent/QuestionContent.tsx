import { IQuestion } from '@/types'
import { Box, Chip, Typography } from '@mui/material'
import Image from 'next/image'
import { UserInformation } from '../UserInformation'

export const QuestionContent = ({
	questionData,
}: {
	questionData: IQuestion
}) => {
	return (
		<Box sx={{ mb: 2, ml: 1 }}>
			<UserInformation questionData={questionData} />
			<Typography sx={{ fontSize: 16 }}>{questionData?.title}</Typography>
			<Typography
				sx={{ mb: 2 }}
				variant='body1'
				dangerouslySetInnerHTML={{
					__html: questionData?.content ?? 'error',
				}}
			/>

			<Box sx={{ mb: 2, display: 'flex' }}>
				{questionData?.images?.map((image) => (
					<Box sx={{ mr: 1 }}>
						<Image
							alt={image?.alt_text ?? ''}
							src={image.image}
							width={64}
							height={64}
						/>
					</Box>
				))}
			</Box>
			<Box>
				{questionData.tags.map((tag) => (
					<Chip key={tag.tag_name} sx={{ mr: 1 }} label={tag.tag_name} />
				))}
			</Box>
		</Box>
	)
}
