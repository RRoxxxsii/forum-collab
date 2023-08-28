import { Box, TextField, InputAdornment, IconButton } from '@mui/material'
import Link from 'next/link'
import React from 'react'
import AccountCircleIcon from '@mui/icons-material/AccountCircle'
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos'

export const QuestionListAskFast = () => {
	return (
		<Box sx={{ width: '100%', mb: 4 }}>
			<Box
				sx={{
					position: 'relative',
					width: 'clamp(300px, 100%, 1200px)',
					height: '100%',
					display: 'flex',
					alignItems: 'center',
				}}>
				<TextField
					fullWidth
					id='input-with-icon-textfield'
					size='medium'
					variant='outlined'
					label='Задайте вопрос'
					InputProps={{
						startAdornment: (
							<InputAdornment position='start'>
								<AccountCircleIcon />
							</InputAdornment>
						),
						endAdornment: (
							<InputAdornment position='end'>
								<IconButton aria-label='Спросить'>
									<Link href={'/ask'}>
										<ArrowForwardIosIcon />
									</Link>
								</IconButton>
							</InputAdornment>
						),
					}}
				/>
			</Box>
		</Box>
	)
}
