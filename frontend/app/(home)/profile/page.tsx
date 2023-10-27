'use client'
import { UserDetailsContext } from '@/providers/UserDetailsProvider'

import { Avatar, Box, Skeleton, Typography } from '@mui/material'
import dayjs from 'dayjs'
import locale from 'dayjs/locale/de'
import relativeTime from 'dayjs/plugin/relativeTime'
import { useContext } from 'react'

export default function ProfilePage() {
	const { userDetails } = useContext(UserDetailsContext)
	dayjs.locale('ru')
	dayjs.extend(relativeTime)

	return (
		<>
			<Box sx={Home} className='flex min-h-screen items-start relative p-4'>
				{userDetails ? (
					<Box sx={{ display: 'flex' }}>
						<Avatar
							sx={{
								minHeight: '100px',
								maxWidth: '200px',
								maxHeigth: '200px',
								aspectRatio: '1/1',
								mr: 1,
							}}
							src={userDetails?.profile_image ?? ''}
							alt={'Картинка профиля' + userDetails?.user_name}>
							{!userDetails?.profile_image &&
								userDetails?.user_name[0].toUpperCase()}
						</Avatar>
						<Box>
							<Typography sx={{ fontSize: '24px' }}>
								{userDetails.user_name}
							</Typography>
							<Typography sx={{ fontSize: '16px' }}>
								{'🎇 Cоздан: ' +
									dayjs(userDetails.created).locale('ru').fromNow()}
							</Typography>
						</Box>
					</Box>
				) : (
					<Skeleton />
				)}
			</Box>
		</>
	)
}

const desktopList = {
	width: 'clamp(300px, 100%, 1200px)',
	display: { md: 'block', xs: 'none' },
}
const mobileList = {
	width: 'clamp(300px, 100%, 1200px)',
	display: { md: 'none', xs: 'block' },
}
const Home = {
	display: 'flex',
	minHeight: 'screen',
	flexDirection: { md: 'row', xs: 'column' },
}
const HomeContainer = {
	width: '100%',
	mt: { md: 3, xs: 4 },
	ml: { md: 2, xs: 0 },
}
