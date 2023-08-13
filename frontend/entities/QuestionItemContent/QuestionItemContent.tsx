import { IQuestionItem } from '@/types/types'
import MoreVertIcon from '@mui/icons-material/MoreVert'
import { Avatar, Box, CardContent, IconButton, Typography } from '@mui/material'

export const QuestionItemContent = ({
	questionData,
}: {
	questionData: Omit<IQuestionItem, 'chips'>
}) => {
	const { description, id, title, user } = questionData

	return (
		<>
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
						Отправлено:{user.username}
					</Typography>
				</Box>
				<Box>
					<IconButton>
						<MoreVertIcon></MoreVertIcon>
					</IconButton>
				</Box>
			</Box>
			<CardContent sx={{ py: 0, px: 2 }}>
				<Typography fontWeight={700} variant='body1' color='text.primary'>
					{title}
				</Typography>
				<Typography variant='body1' color='text.secondary'>
					{description}
				</Typography>
			</CardContent>
		</>
	)
}
