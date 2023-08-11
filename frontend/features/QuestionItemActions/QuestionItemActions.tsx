'use client'
import { IChip } from '@/widgets/QuestionList/QuestionList'
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

export const QuestionItemActions = ({ chips }: { chips: IChip[] }) => {
	return (
		<CardActions sx={{ width: '100%', justifyContent: 'space-between' }}>
			<Box
				sx={{
					display: 'flex',
					justifyContent: 'center',
					flexWrap: 'wrap',
					listStyle: 'none',
					p: 0.5,
					m: 0,
				}}
				component='ul'>
				{chips.map((chip) => {
					return (
						<ListItem sx={{ p: 0, mr: 1, cursor: 'pointer' }} key={chip.key}>
							<Chip label={chip.label} />
						</ListItem>
					)
				})}
			</Box>
			<Box>
				<IconButton aria-label='comments'>
					<Typography sx={{ mr: 1 }}>10</Typography>
					<TextsmsIcon />
				</IconButton>
			</Box>
		</CardActions>
	)
}
