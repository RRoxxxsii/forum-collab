import { Card } from '@mui/material'
import Link from 'next/link'
import React from 'react'

export const QuestionItemWrapper = ({
	children,
	href,
}: {
	children: React.ReactNode
	href: string
}) => {
	return (
		<Card
			sx={{
				width: 'clamp(300px, 100%, 1200px)',
				transition: 'border-color 0.3s ease-in-out',
				border: '1px solid transparent',
				'&:hover': { border: 1, transition: 0.3, borderColor: 'teal' },
				cursor: 'pointer',
				mb: 2,
			}}>
			<Link href={href}>{children}</Link>
		</Card>
	)
}
