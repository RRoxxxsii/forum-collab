import { IUser } from '@/types'
import { Box, Avatar } from '@mui/material'

export const ProfileAvatar = ({ profileData }: { profileData: IUser }) => {
	return (
		<Box sx={{ display: 'flex', height: '100%', mb: 3 }}>
			<Avatar
				sx={{
					borderRadius: 0,
					mr: 1,
					height: 128,
					width: 128,
					aspectRatio: '1/1',
				}}
				src={profileData?.profile_image ?? ''}
				alt={'Картинка профиля' + profileData?.user_name}>
				{!profileData?.profile_image && profileData?.user_name[0].toUpperCase()}
			</Avatar>
		</Box>
	)
}
