'use client'
import { Tag } from '@/shared/Tag'
import { IUser } from '@/types'
import { Cake, Verified } from '@mui/icons-material'
import { Avatar, Box, Chip, Skeleton, Tooltip, Typography } from '@mui/material'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { useEffect, useState } from 'react'
import { toast } from 'react-toastify'

export default function ProfilePage({ params }: { params: { slug: string } }) {
	const [profileData, setProfileData] = useState<IUser | null>(null)
	const userId = params.slug

	dayjs.extend(relativeTime)

	const getProfile = async () => {
		try {
			const response = await fetch('/api/account/profile', {
				method: 'POST',
				body: JSON.stringify({ userId: userId }),
			})

			const result = await response.json()

			if (!response.ok) {
				throw new Error(
					result?.detail ?? result ?? 'Ошибка при загрузке профиля'
				)
			}

			setProfileData(result)
		} catch (error) {
			if (error instanceof Error) {
				toast.error(error.message)
			}
			if (typeof error === 'string') {
				toast.error(error)
			}
		}
	}

	useEffect(() => {
		getProfile()
	}, [])

	return (
		<>
			<Box className='flex flex-col min-h-screen items-start relative p-4 max-w-4xl'>
				{profileData ? (
					<>
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
								{!profileData?.profile_image &&
									profileData?.user_name[0].toUpperCase()}
							</Avatar>
							<Box sx={{ ml: 1 }}>
								<Box sx={{ display: 'flex', alignItems: 'center' }}>
									<Typography sx={{ fontSize: 24, mr: 1 }}>
										{profileData?.user_name}{' '}
									</Typography>
									{profileData.is_active && (
										<Tooltip title={'Подтверждён'}>
											<Verified
												color='secondary'
												sx={{ width: 20, height: 20, mb: 1 }}
											/>
										</Tooltip>
									)}
								</Box>
								{profileData.is_banned && (
									<Chip
										sx={{ mb: 1 }}
										label={'Пользователь забанен'}
										color={'error'}
									/>
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
						</Box>
						<Box sx={{ display: 'flex', alignItems: 'center' }}>
							<Box>
								<Typography sx={{ mb: 1, fontSize: 24 }}>
									Лучшие теги
								</Typography>
								<Box>
									{profileData?.best_tags?.map((tag) => (
										<Tag key={tag.tag_name} tagData={tag} />
									))}
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
const Home = {
	display: 'flex',
	minHeight: 'screen',
	flexDirection: { md: 'row', xs: 'column' },
}
