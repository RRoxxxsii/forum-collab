import { CategoryTabs } from '@/widgets/CategoryTabs'
import { QuestionList } from '@/widgets/QuestionList'
import { AccountCircle } from '@mui/icons-material'
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos'
import {
	Box,
	Button,
	IconButton,
	InputAdornment,
	TextField,
} from '@mui/material'
import Link from 'next/link'

export default async function HomePage() {
	return (
		<Box className='flex min-h-screen items-start max-h-80 relative'>
			<CategoryTabs />
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
										<IconButton aria-label='Спросить'>
											<Link href={'/ask'}>
												<ArrowForwardIosIcon />
											</Link>
										</IconButton>
									</InputAdornment>
								),
							}}
						/>
					</Box>
				</Box>
				<Box sx={{ mt: 4, width: 'clamp(300px, 100%, 1200px)' }}>
					<QuestionList />
				</Box>
			</Box>
		</Box>
	)
}
