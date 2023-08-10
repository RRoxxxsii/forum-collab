'use client'
import { AccountCircle } from '@mui/icons-material'
import AccessTimeIcon from '@mui/icons-material/AccessTime'
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos'
import MoreVertIcon from '@mui/icons-material/MoreVert'
import StarIcon from '@mui/icons-material/Star'
import TextsmsIcon from '@mui/icons-material/Textsms'
import WhatshotIcon from '@mui/icons-material/Whatshot'
import {
	Avatar,
	Box,
	Button,
	Card,
	CardActions,
	CardContent,
	Chip,
	IconButton,
	InputAdornment,
	TextField,
	Typography,
	styled,
} from '@mui/material'
import Tab from '@mui/material/Tab'
import Tabs from '@mui/material/Tabs'
import { useState } from 'react'

interface ChipData {
	key: number
	label: string
}

const ListItem = styled('li')(({ theme }) => ({
	margin: theme.spacing(0.5),
}))

export default function HomePage() {
	const [value, setValue] = useState(0)

	const handleChange = (event: React.SyntheticEvent, newValue: number) => {
		setValue(newValue)
	}
	const [chipData, setChipData] = useState<readonly ChipData[]>([
		{ key: 0, label: 'Angular' },
		{ key: 1, label: 'jQuery' },
		{ key: 2, label: 'Polymer' },
		{ key: 3, label: 'React' },
		{ key: 4, label: 'Vue.js' },
	])

	return (
		<Box className='flex min-h-screen items-start max-h-80 relative'>
			<Box className='w-32 h-screen'>
				<Box className='flex flex-col justify-between items-center fixed'>
					<Tabs
						orientation='vertical'
						value={value}
						onChange={handleChange}
						aria-label='icon label tabs example'>
						<Tab icon={<AccessTimeIcon />} label='ПОСЛЕДНИЕ' />
						<Tab icon={<WhatshotIcon />} label='ОТКРЫТЫЕ' />
						<Tab icon={<StarIcon />} label='ЛУЧШИЕ' />
					</Tabs>
				</Box>
			</Box>
			<Box sx={{ px: 3, width: '100%' }}>
				<Box sx={{ display: 'flex' }}>
					<Box
						sx={{
							position: 'relative',
							width: 'clamp(300px, 100%, 1200px)',
							height: '100%',
							display: 'flex',
							alignItems: 'center',
						}}>
						<TextField
							fullWidth
							id='input-with-icon-textfield'
							size='medium'
							variant='outlined'
							label='Задайте вопрос'
							InputProps={{
								startAdornment: (
									<InputAdornment position='start'>
										<AccountCircle />
									</InputAdornment>
								),
								endAdornment: (
									<InputAdornment position='end'>
										<Button>
											<ArrowForwardIosIcon />
										</Button>
									</InputAdornment>
								),
							}}
						/>
					</Box>
				</Box>
				<Box sx={{ mt: 4, width: 'clamp(300px, 100%, 1200px)' }}>
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
								циклом пробегаешься по массиву если элемент предыдущий n - 1
								больше следующего то ищешь сумму и так далее что-то в этом роде
							</Typography>
						</CardContent>
						<CardActions
							sx={{ width: '100%', justifyContent: 'space-between' }}>
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
										<ListItem
											sx={{ p: 0, mr: 1, cursor: 'pointer' }}
											key={data.key}>
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
				</Box>
			</Box>
		</Box>
	)
}
