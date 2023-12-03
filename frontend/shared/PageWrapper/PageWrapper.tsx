import { Box } from '@mui/material'
import React from 'react'

export const PageWrapper = ({ children }: { children: React.ReactNode }) => {
	return <Box sx={{ minHeight: '80vh' }}>{children}</Box>
}
