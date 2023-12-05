import { Transliterate } from '@/shared/utils/Transliterate'
import { IQuestion } from '@/types'
import { Box, Chip } from '@mui/material'
import Link from 'next/link'

export const QuestionCardTags = ({
	questionData,
}: {
	questionData: IQuestion
}) => {
	return (
		<Box sx={{ mb: 2 }}>
			{questionData.tags.map((tag) => (
				<Link href={`/questions/?tags=${Transliterate(tag?.tag_name)}`}>
					<Chip
						label={tag.tag_name}
						sx={{
							background: '#292929',
							color: '#e1e1e1',
							'&:hover': { transition: 0.3, background: '#363636' },
						}}
					/>
				</Link>
			))}
		</Box>
	)
}
