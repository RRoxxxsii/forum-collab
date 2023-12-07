'use client'
import { ProfileAvatar } from '@/components/Profile/ProfileAvatar'
import { ProfileHeader } from '@/components/Profile/ProfileHeader'
import { ProfileTags } from '@/components/Profile/ProfileTags'
import { IUser } from '@/types'
import { Box, Skeleton } from '@mui/material'
import { useEffect, useState } from 'react'
import { toast } from 'react-toastify'

export default function ProfilePage({ params }: { params: { slug: string } }) {
	const [profileData, setProfileData] = useState<IUser | null>(null)
	const userId = params.slug

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
						<Box sx={{ display: 'flex' }}>
							<ProfileAvatar profileData={profileData} />
							<ProfileHeader profileData={profileData} />
						</Box>
						<ProfileTags profileData={profileData} />
					</>
				) : (
					<>
						<Box sx={{ display: 'flex', mb: 4 }}>
							<Skeleton
								sx={{ mr: 2 }}
								variant='rectangular'
								width={128}
								height={128}
							/>
							<Skeleton variant='rectangular' width={200} height={128} />
						</Box>
						<Skeleton variant='rectangular' width={344} height={128} />
					</>
				)}
			</Box>
		</>
	)
}
