'use client'

import { NotificationContext } from '@/providers/NotificationsProvider'
import { ModalComponent } from '@/shared/Modal'
import { INotificationLevelType } from '@/types'
import { Alert, AlertColor, Typography } from '@mui/material'
import dayjs from 'dayjs'
import ru from 'dayjs/locale/ru'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { useContext, useState } from 'react'
import './styles.scss'
export const NotificationsModal = () => {
	const isOpen = useSearchParams().has('notifications')
	const router = useRouter()

	const { notifications, setNotifications } = useContext(NotificationContext)
	console.log(notifications)
	const [value, setValue] = useState<number>(0)

	const handleClose = () => {
		router.back()
	}

	const notificationLevelStrings: Record<INotificationLevelType, AlertColor> = {
		info: 'info',
		fail: 'error',
		success: 'success',
		warning: 'warning',
	}
	if (!isOpen) return null

	return (
		<ModalComponent handleClose={handleClose}>
			<div className='p-2'>
				<Typography sx={{ fontSize: 24 }}>Уведомления</Typography>
				{notifications.length !== 0 ? (
					notifications.map((notification) => (
						<Alert
							sx={{ mb: 1 }}
							color={notificationLevelStrings[notification.level]}>
							<Link href=''>
								<Typography>
									{notification.sender} {notification.text}
								</Typography>
								<Typography></Typography>
								<Typography sx={{ fontSize: 12 }}>
									{dayjs(notification.creation_date).locale(ru).fromNow()}
								</Typography>
							</Link>
						</Alert>
					))
				) : (
					<Typography>У вас пока нет уведомлений</Typography>
				)}
			</div>
		</ModalComponent>
	)
}
