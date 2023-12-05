import { ITag } from '@/types'
import { Chip } from '@mui/material'
import Link from 'next/link'

export const Tag = ({ tagData }: { tagData: ITag }) => {
	return (
		<Link href={`/questions/tags=${tagData.tag_name}`}>
			<Chip
				sx={{ width: '100%' }}
				label={tagData.tag_name}
				color={tagData.is_relevant ? 'primary' : 'default'}
			/>
		</Link>
	)
}
