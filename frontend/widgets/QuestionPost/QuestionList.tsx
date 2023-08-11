'use client'
import MoreVertIcon from '@mui/icons-material/MoreVert'
import TextsmsIcon from '@mui/icons-material/Textsms'
import {
	Avatar,
	Box,
	Card,
	CardActions,
	CardContent,
	Chip,
	IconButton,
	Typography,
	styled,
} from '@mui/material'
import { useState } from 'react'

interface ChipData {
	key: number
	label: string
}

const ListItem = styled('li')(({ theme }) => ({
	margin: theme.spacing(0.5),
}))

export const QuestionList = () => {
	const [chipData, setChipData] = useState<readonly ChipData[]>([
		{ key: 0, label: 'Angular' },
		{ key: 1, label: 'jQuery' },
		{ key: 2, label: 'Polymer' },
		{ key: 3, label: 'React' },
		{ key: 4, label: 'Vue.js' },
	])
	return (
		<Card sx={{ width: 'clamp(300px, 100%, 1200px)' }}>
			<Box
				sx={{
					ml: 2,
					mt: 1,
					display: 'flex',
					justifyContent: 'space-between',
					alignItems: 'center',
				}}>
				<Box sx={{ display: 'flex' }}>
					<Avatar sx={{ width: 20, height: 20, mr: 1 }}></Avatar>
					<Typography variant='body2' color='text.secondary'>
						Отправлено: Илья Муромец
					</Typography>
				</Box>
				<Box>
					<IconButton>
						<MoreVertIcon></MoreVertIcon>
					</IconButton>
				</Box>
			</Box>
			<CardContent>
				<Typography fontWeight={700} variant='body1' color='text.primary'>
					че за пиздец блять хахахахвхвхыхахахахвх Илья Муромец а ты
				</Typography>
				<Typography variant='body1' color='text.secondary'>
					циклом пробегаешься по массиву если элемент предыдущий n - 1 больше
					следующего то ищешь сумму и так далее что-то в этом роде
				</Typography>
			</CardContent>
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
					{chipData.map((data) => {
						return (
							<ListItem sx={{ p: 0, mr: 1, cursor: 'pointer' }} key={data.key}>
								<Chip label={data.label} />
							</ListItem>
						)
					})}
				</Box>
				<Box>
					<IconButton aria-label='comments'>
						<Typography sx={{ mr: 1 }}>10</Typography>
						<TextsmsIcon />
					</IconButton>
					{/* <IconButton aria-label='share'>
								<ShareIcon />
							</IconButton> */}
				</Box>
			</CardActions>
		</Card>
	)
}
