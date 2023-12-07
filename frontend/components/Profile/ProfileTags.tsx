import { Tag } from '@/shared/Tag'
import { IUser } from '@/types'

import { Box, Typography } from '@mui/material'

export const ProfileTags = ({ profileData }: { profileData: IUser }) => {
	return (
		<Box sx={{ display: 'flex', alignItems: 'center' }}>
			<Box>
				<Typography sx={{ mb: 1, fontSize: 24 }}>Лучшие теги</Typography>
				<Box sx={{ display: 'flex' }}>
					{profileData?.best_tags?.map((tag) => (
						<Tag key={tag.tag_name} tagData={tag} />
					))}
				</Box>
			</Box>
		</Box>
	)
}
