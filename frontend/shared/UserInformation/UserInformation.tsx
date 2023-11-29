'use client'
import { IQuestion } from '@/types'

import { Avatar, Box, Tooltip, Typography } from '@mui/material'
import { green } from '@mui/material/colors'
import dayjs from 'dayjs'
import ru from 'dayjs/locale/ru'
import relativeTime from 'dayjs/plugin/relativeTime'

export const UserInformation = ({
	questionData,
}: {
	questionData: IQuestion
}) => {
	dayjs.locale(ru)
	dayjs.extend(relativeTime)

	return (
		<Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
			<Avatar
				sx={{
					width: 20,
					height: 20,
					fontSize: 16,
					bgcolor: green[400],
					marginRight: 1,
				}}
				aria-label='recipe'
				src={questionData?.user?.profile_image ?? ''}>
				{questionData?.user?.profile_image
					? ''
					: questionData?.user?.user_name[0].toUpperCase()}
			</Avatar>
			<Typography sx={{ marginRight: 1 }} variant='caption'>
				{questionData?.user?.user_name ?? 'Гость'}
			</Typography>
			<Tooltip
				placement='right'
				title={`${
					questionData.updated_date
						? `Изменён ${
								dayjs(questionData?.updated_date).toNow(true) + ' назад' ??
								'...'
						  }`
						: `Создан ${
								dayjs(questionData?.creation_date).toNow(true) + ' назад' ??
								'...'
						  }`
				}`}>
				<Typography variant='body2' sx={{ ml: 1 }} color='gray' fontSize={12}>
					{dayjs(questionData?.creation_date).toNow(true) + ' назад'}
				</Typography>
			</Tooltip>
		</Box>
	)
}
