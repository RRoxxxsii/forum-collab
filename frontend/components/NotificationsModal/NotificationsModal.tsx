'use client'
import { NotificationContext } from '@/providers/NotificationsProvider'
import { ModalComponent } from '@/shared/Modal'
import { Paper, Typography } from '@mui/material'
import { useRouter, useSearchParams } from 'next/navigation'
import { useContext, useState } from 'react'
import './styles.scss'

export const NotificationsModal = ({}: {}) => {
	const isOpen = useSearchParams().has('notifications')
	const router = useRouter()

	const { notifications } = useContext(NotificationContext)

	const [value, setValue] = useState<number>(0)

	const handleClose = () => {
		router.back()
	}
	console.log(notifications)
	if (!isOpen) return null

	return (
		<ModalComponent handleClose={handleClose}>
			<div className='p-2'>
				<Typography sx={{ fontSize: 24 }}>Уведомления</Typography>
				{notifications.map((notification) => (
					<Paper>
						{notification.level}
						{notification.text}
					</Paper>
				))}
			</div>
		</ModalComponent>
	)
}
