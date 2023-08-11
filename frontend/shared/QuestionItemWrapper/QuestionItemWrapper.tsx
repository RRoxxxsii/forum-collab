import { Card } from '@mui/material'
import React from 'react'

export const QuestionItemWrapper = ({
	children,
}: {
	children: React.ReactNode
}) => {
	return (
		<Card
			sx={{ width: 'clamp(300px, 100%, 1200px)', mb: 2 }}
			className='hover:bg-gray-200'>
			{children}
		</Card>
	)
}
