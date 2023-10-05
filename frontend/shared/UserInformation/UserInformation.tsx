import { IQuestion } from '@/types/types'
import { Box, Avatar, Typography } from '@mui/material'
import { green, red } from '@mui/material/colors'
import dayjs from 'dayjs'
import React from 'react'

export const UserInformation = ({
	questionData,
}: {
	questionData: IQuestion
}) => {
	return (
		<Box sx={{ display: 'flex' }}>
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
				{questionData?.user?.profile_image
					? ''
					: questionData?.user?.user_name[0]}
			</Avatar>
			<Typography sx={{ marginRight: 1 }} variant='caption'>
				{questionData?.user?.user_name || 'Гость'}
			</Typography>
			<Typography sx={{ color: 'GrayText' }} variant='caption'>
				{dayjs(questionData?.creation_date).format('DD-MM-YYYY')}
			</Typography>
		</Box>
	)
}
