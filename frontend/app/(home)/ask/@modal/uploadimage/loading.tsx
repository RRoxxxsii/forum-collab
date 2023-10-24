import { Box, Skeleton } from '@mui/material'

export default function Loading() {
	return (
		<Box sx={{ margin: '0 auto' }}>
			<Box sx={askPageWrapper}>
				<Skeleton height={800} width={600} />
			</Box>
		</Box>
	)
}

const askPageWrapper = {
	width: '100%',
	padding: { md: 3, xs: 0 },
}
