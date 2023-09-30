'use client'

import theme from '@/shared/theme/theme'
import { IQuestion } from '@/types/types'
import TextsmsIcon from '@mui/icons-material/Textsms'
import {
	Box,
	CardActions,
	Chip,
	IconButton,
	Typography,
	styled,
} from '@mui/material'

const ListItem = styled('li')(({ theme }) => ({
	margin: theme.spacing(0.5),
}))

export const QuestionItemActions = ({
	questionData,
}: {
	questionData: IQuestion
}) => {
	return (
		<CardActions sx={{ width: '100%', justifyContent: 'space-between', p: 0 }}>
			<Box
				sx={{
					display: 'flex',
					justifyContent: 'flex-start',
					flexWrap: 'nowrap',
					listStyle: 'none',
					m: 0,
					flex: '50%',
				}}
				component='ul'>
				{questionData?.tags.map((tag) => {
					return (
						<ListItem
							sx={{ p: 0, mr: 1, cursor: 'pointer', flexWrap: 'nowrap' }}
							key={tag.tag_name}>
							<Chip key={tag.tag_name} label={tag.tag_name} />
						</ListItem>
					)
				})}
			</Box>
			<Box sx={{ display: 'flex', flex: '50%', justifyContent: 'flex-end' }}>
				<IconButton aria-label='comments'>
					<Typography sx={{ mr: 1 }}>{questionData?.answers_amount}</Typography>
					<TextsmsIcon />
				</IconButton>
			</Box>
		</CardActions>
	)
}
