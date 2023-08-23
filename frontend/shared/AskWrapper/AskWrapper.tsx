import { AskTabs } from '@/widgets/AskTabs'
import { Typography, Paper } from '@mui/material'
import React from 'react'

export const AskWrapper = ({ children }: { children: React.ReactNode }) => {
	return (
		<>
			<Typography sx={{ mb: 2 }} component='h1'>
				Создать вопрос
			</Typography>
			<Paper
				elevation={2}
				variant={'elevation'}
				sx={{
					p: 2,
					position: 'relative',
					width: 'clamp(300px, 100%, 1200px)',
					height: '100%',
					minHeight: '400px',
					alignItems: 'center',
				}}>
				<AskTabs />
				{children}
			</Paper>
		</>
	)
}
