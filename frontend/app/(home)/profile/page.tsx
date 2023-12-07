'use client'
import { ProfileAvatar } from '@/components/Profile/ProfileAvatar'
import { ProfileHeader } from '@/components/Profile/ProfileHeader'
import { ProfileTags } from '@/components/Profile/ProfileTags'
import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { Box, Skeleton } from '@mui/material'
import { useContext } from 'react'

export default function ProfilePage() {
	const { userDetails } = useContext(UserDetailsContext)

	return (
		<>
			<Box className='flex flex-col min-h-screen items-start relative p-4'>
				{userDetails ? (
					<>
						<Box sx={{ display: 'flex' }}>
							<ProfileAvatar profileData={userDetails} />
							<ProfileHeader profileData={userDetails} />
						</Box>
						<ProfileTags profileData={userDetails} />
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
