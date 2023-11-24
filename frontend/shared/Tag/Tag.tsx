import { ITag } from '@/types'
import { Chip } from '@mui/material'

export const Tag = ({ tagData }: { tagData: ITag }) => {
	return (
		<Chip
			label={tagData.tag_name}
			color={tagData.is_relevant ? 'primary' : 'default'}
		/>
	)
}
