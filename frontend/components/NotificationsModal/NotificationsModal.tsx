'use client'
import { ModalComponent } from '@/shared/Modal'
import { Typography, Box, Paper } from '@mui/material'
import { useRouter, useSearchParams } from 'next/navigation'
import { useState } from 'react'
import './styles.scss'

export const NotificationsModal = ({}: {}) => {
	const isOpen = useSearchParams().has('notifications')
	const router = useRouter()

	const [value, setValue] = useState<number>(0)

	const handleClose = () => {
		router.back()
	}

	if (!isOpen) return null

	return (
		<ModalComponent handleClose={handleClose}>
			<div className='p-2'>
				<Typography sx={{ fontSize: 24 }}>Уведомления</Typography>
				<Paper>XD</Paper>
			</div>
		</ModalComponent>
	)
}
