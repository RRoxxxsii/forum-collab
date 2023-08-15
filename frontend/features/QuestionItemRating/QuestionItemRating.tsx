import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward'
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward'
import { Box, IconButton, Typography } from '@mui/material'

export const QuestionItemRating = () => {
	return (
		<Box
			sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
			<IconButton>
				<ArrowUpwardIcon></ArrowUpwardIcon>
			</IconButton>
			<Typography fontWeight={700}>110</Typography>
			<IconButton>
				<ArrowDownwardIcon></ArrowDownwardIcon>
			</IconButton>
		</Box>
	)
}
