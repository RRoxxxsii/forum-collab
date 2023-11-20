'use client'
import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { Tag } from '@/shared/Tag'
import { Cake, Check } from '@mui/icons-material'

import { Avatar, Box, Chip, Skeleton, Tooltip, Typography } from '@mui/material'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { useContext } from 'react'

export default function ProfilePage() {
	const { userDetails } = useContext(UserDetailsContext)
	dayjs.locale('ru')
	dayjs.extend(relativeTime)

	return (
		<>
			<Box
				sx={Home}
				className='flex flex-col min-h-screen items-start relative p-4'>
				{userDetails ? (
					<>
						<Box sx={{ display: 'flex', height: '100%', mb: 3 }}>
							<Avatar
								sx={{
									borderRadius: 0,
									mr: 1,
									height: 64,
									width: 64,
									aspectRatio: '1/1',
								}}
								src={userDetails?.profile_image ?? ''}
								alt={'Картинка профиля' + userDetails?.user_name}>
								{!userDetails?.profile_image &&
									userDetails?.user_name[0].toUpperCase()}
							</Avatar>
							<Box>
								<Box sx={{ display: 'flex', alignItems: 'center' }}>
									{userDetails.is_active && (
										<Tooltip title={'Подтверждён'}>
											<Check
												sx={{ width: 20, height: 20, mr: 1 }}
												color={'success'}
											/>
										</Tooltip>
									)}
									<Typography sx={{ fontSize: '24px' }}>
										{userDetails?.user_name}
									</Typography>
									{userDetails.is_banned && (
										<Chip label={'Забанен'} color={'error'} />
									)}
								</Box>
								<Box sx={{ display: 'flex', alignItems: 'end' }}>
									<Cake sx={{ width: 20, height: 20, mb: 0.5, mr: 1 }} />
									<Typography sx={{ fontSize: '16px' }}>
										{' Cоздан: ' +
											dayjs(userDetails?.created)
												.locale('ru')
												.fromNow()}
									</Typography>
								</Box>
							</Box>
						</Box>
						<Box>
							<Typography sx={{ mb: 1, fontSize: 24 }}>Статистика</Typography>

							<Box
								sx={{
									display: 'flex',
									mb: 3,
									borderRadius: 2,
									border: '1px solid #3b3b3b',
									p: 1,
								}}>
								<Typography sx={{ mr: 3, fontSize: 16 }}>
									Карма: {userDetails.karma}
								</Typography>
								<Typography sx={{ fontSize: 16 }}>
									Лучших ответов: {userDetails.amount_solved}
								</Typography>
							</Box>
							<Box sx={{ display: 'flex', alignItems: 'center' }}>
								<Box>
									<Typography>Лучшие теги</Typography>
									<Box
										sx={{ borderRadius: 2, border: '1px solid #3b3b3b', p: 1 }}>
										{userDetails?.best_tags?.map((tag) => (
											<Tag tagData={tag} />
										))}
									</Box>
								</Box>
							</Box>
						</Box>
					</>
				) : (
					<Skeleton />
				)}
			</Box>
		</>
	)
}
;['fewktgwqe', 'qwetkpqt', 'etokwqetkq']

const desktopList = {
	width: 'clamp(300px, 100%, 1200px)',
	display: { md: 'block', xs: 'none' },
}
const mobileList = {
	width: 'clamp(300px, 100%, 1200px)',
	display: { md: 'none', xs: 'block' },
}
const Home = {
	minHeight: 'screen',
}
const HomeContainer = {
	width: '100%',
	mt: { md: 3, xs: 4 },
	ml: { md: 2, xs: 0 },
}
