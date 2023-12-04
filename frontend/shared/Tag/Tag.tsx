import { ITag } from '@/types'
import { Chip } from '@mui/material'

export const Tag = ({ tagData }: { tagData: ITag }) => {
	return (
		<Chip
			sx={{ width: '100%' }}
			label={tagData.tag_name}
			color={tagData.is_relevant ? 'primary' : 'default'}
		/>
	)
}
