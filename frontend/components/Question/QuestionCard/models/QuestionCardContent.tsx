import { ImageModal } from '@/components/ImageModal'
import { IQuestion } from '@/types'
import { Box, Chip, Typography } from '@mui/material'
import { ImageButton } from '../../../../shared/ImageButton'
import { UserInformation } from '../../../../shared/UserInformation'

export const QuestionCardContent = ({
	questionData,
}: {
	questionData: IQuestion
}) => {
	return (
		<Box sx={{ mb: 2, ml: 1 }}>
			<ImageModal imageUrl='' />
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
						<ImageButton
							imageAlt={image?.alt_text ?? ''}
							imageUrl={image.image}
							width={128}
							height={128}
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
