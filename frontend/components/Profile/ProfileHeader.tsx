import { IUser } from '@/types'
import { Cake, Verified } from '@mui/icons-material'
import { Box, Chip, Tooltip, Typography } from '@mui/material'
import dayjs from 'dayjs'

export const ProfileHeader = ({ profileData }: { profileData: IUser }) => {
	return (
		<Box sx={{ ml: 1 }}>
			<Box sx={{ display: 'flex', alignItems: 'center' }}>
				<Typography sx={{ fontSize: 24, mr: 1 }}>
					{profileData?.user_name}{' '}
				</Typography>
				{profileData.is_active && (
					<Tooltip title={'Подтверждён'}>
						<Verified color='secondary' sx={{ width: 20, height: 20, mb: 1 }} />
					</Tooltip>
				)}
			</Box>
			{profileData.is_banned && (
				<Chip sx={{ mb: 1 }} label={'Пользователь забанен'} color={'error'} />
			)}
			<Box sx={{ display: 'flex', alignItems: 'end', mb: 1 }}>
				<Tooltip title={'Дата создания аккаунта'}>
					<Cake sx={{ width: 20, height: 20, mb: 0.6, mr: 1 }} />
				</Tooltip>
				<Typography sx={{ fontSize: '16px' }}>
					{dayjs(profileData?.created).format('DD.MM.YYYY')}
				</Typography>
			</Box>
			<Typography sx={{ mr: 3, fontSize: 16 }}>
				Карма: {profileData.karma}
			</Typography>
			<Typography sx={{ fontSize: 16 }}>
				Лучших ответов: {profileData.amount_solved}
			</Typography>
		</Box>
	)
}
