'use client'

import { IChip } from '@/types/types'
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
				{chips.map((chip) => {
					return (
						<ListItem sx={{ p: 0, mr: 1, cursor: 'pointer' }} key={chip.tag}>
							<Chip key={chip.tag} label={chip.tag} />
						</ListItem>
					)
				})}
			</Box>
			<Box sx={{ display: 'flex', flex: '50%', justifyContent: 'flex-end' }}>
				<IconButton aria-label='comments'>
					<Typography sx={{ mr: 1 }}>10</Typography>
					<TextsmsIcon />
				</IconButton>
			</Box>
		</CardActions>
	)
}
