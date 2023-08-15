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
			<Box sx={{ display: 'flex', width: '100%' }}>
				<Box
					sx={{
						display: 'flex',
						flexDirection: 'column',
						width: '100%',
						pb: 1,
						px: 1,
					}}>
					<Box
						sx={{
							display: 'flex',
							justifyContent: 'space-between',
							alignItems: 'center',
							width: '100%',
						}}>
						<Box
							sx={{
								width: '100%',
								display: 'flex',
								justifyContent: 'space-between',
								alignItems: 'center',
							}}>
							<Box
								sx={{ display: 'flex', width: '100%', alignItems: 'center' }}>
								<Avatar sx={{ width: 16, height: 16, mr: 1 }}></Avatar>
								<Typography
									variant='body2'
									fontSize={12}
									color='text.secondary'>
									Отправлено: {user.username}{' '}
								</Typography>
								<Typography
									variant='body2'
									sx={{ ml: 1 }}
									color='gray'
									fontSize={12}>
									4 Дня назад
								</Typography>
							</Box>
							<Box>
								<IconButton>
									<MoreVertIcon></MoreVertIcon>
								</IconButton>
							</Box>
						</Box>
					</Box>
					<CardContent sx={{ p: 0, ':last-child': { pb: 0 } }}>
						<Typography fontWeight={700} variant='body1' color='text.primary'>
							{title}
						</Typography>
						<Typography variant='body1' color='text.secondary'>
							{description}
						</Typography>
					</CardContent>
				</Box>
			</Box>
		</>
	)
}
