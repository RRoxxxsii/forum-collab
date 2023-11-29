'use client'
import { Tag } from '@/shared/Tag'
import { IUser } from '@/types'
import { Cake, Check } from '@mui/icons-material'
import { Avatar, Box, Chip, Skeleton, Tooltip, Typography } from '@mui/material'
import dayjs from 'dayjs'
import ru from 'dayjs/locale/ru'
import relativeTime from 'dayjs/plugin/relativeTime'
import Link from 'next/link'
import { useEffect, useState } from 'react'
import { toast } from 'react-toastify'

export default function ProfilePage({ params }: { params: { slug: string } }) {
	const [profileData, setProfileData] = useState<IUser | null>(null)
	const userId = params.slug

	console.log(params)
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
			<Box className='flex flex-col min-h-screen items-start relative p-4'>
				{profileData ? (
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
								src={profileData?.profile_image ?? ''}
								alt={'Картинка профиля' + profileData?.user_name}>
								{!profileData?.profile_image &&
									profileData?.user_name[0].toUpperCase()}
							</Avatar>
							<Box>
								<Box sx={{ display: 'flex', alignItems: 'center' }}>
									{profileData.is_active && (
										<Tooltip title={'Подтверждён'}>
											<Check
												sx={{ width: 20, height: 20, mr: 1 }}
												color={'success'}
											/>
										</Tooltip>
									)}
									<Link
										href={`/profile/:${profileData.id}`}
										className='text-lg'>
										{profileData?.user_name}
									</Link>
									{profileData.is_banned && (
										<Chip sx={{ ml: 1 }} label={'Забанен'} color={'error'} />
									)}
								</Box>
								<Box sx={{ display: 'flex', alignItems: 'end' }}>
									<Cake sx={{ width: 20, height: 20, mb: 0.5, mr: 1 }} />
									<Typography sx={{ fontSize: '16px' }}>
										{' Cоздан: ' +
											dayjs(profileData?.created)
												?.locale(ru)
												?.fromNow()}
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
									Карма: {profileData.karma}
								</Typography>
								<Typography sx={{ fontSize: 16 }}>
									Лучших ответов: {profileData.amount_solved}
								</Typography>
							</Box>
							<Box sx={{ display: 'flex', alignItems: 'center' }}>
								<Box>
									<Typography>Лучшие теги</Typography>
									<Box
										sx={{ borderRadius: 2, border: '1px solid #3b3b3b', p: 1 }}>
										{profileData?.best_tags?.map((tag) => (
											<Tag key={tag.tag_name} tagData={tag} />
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
const Home = {
	display: 'flex',
	minHeight: 'screen',
	flexDirection: { md: 'row', xs: 'column' },
}
