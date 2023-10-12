import { IQuestion } from '@/types/types'
import MoreVertIcon from '@mui/icons-material/MoreVert'
import { Avatar, Box, CardContent, IconButton, Typography } from '@mui/material'
import { green } from '@mui/material/colors'
import dayjs from 'dayjs'
import ru from 'dayjs/locale/ru'
import relativeTime from 'dayjs/plugin/relativeTime'
export const QuestionItemContent = ({
	questionData,
}: {
	questionData: IQuestion
}) => {
	const {
		answers,
		content,
		creation_date,
		id,
		images,
		is_solved,
		rating,
		title,
		user,
	} = questionData
	dayjs.locale(ru)
	dayjs.extend(relativeTime)
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
								<Avatar
									sx={{
										width: 18,
										height: 18,
										fontSize: 12,
										bgcolor: green[500],
										marginRight: 1,
									}}
									aria-label='recipe'
									src={
										questionData?.user?.profile_image
											? questionData?.user?.profile_image
											: ''
									}>
									{!questionData?.user?.profile_image &&
										questionData?.user?.user_name[0]}
								</Avatar>
								<Typography
									variant='body2'
									fontSize={12}
									color='text.secondary'>
									Отправлено: {user.user_name ?? 'Гость'}
								</Typography>
								<Typography
									variant='body2'
									sx={{ ml: 1 }}
									color='gray'
									fontSize={12}>
									{dayjs(creation_date).toNow(true) + ' назад'}
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
						<Typography
							dangerouslySetInnerHTML={{ __html: content }}
							variant='body1'
							color='text.secondary'></Typography>
					</CardContent>
				</Box>
			</Box>
		</>
	)
}
