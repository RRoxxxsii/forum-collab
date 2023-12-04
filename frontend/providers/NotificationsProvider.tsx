'use client'
import { fetchNotifications } from '@/shared/api/fetchData'
import { INotifications } from '@/types'
import React, {
	Dispatch,
	SetStateAction,
	createContext,
	useEffect,
	useState,
} from 'react'

const initialState: INotifications[] = []

interface NotificationsProviderProps {
	notifications: INotifications[]
	setNotifications: Dispatch<SetStateAction<INotifications[]>>
}

export const NotificationContext = createContext<NotificationsProviderProps>({
	notifications: initialState,
	setNotifications: () => {},
})

export const NotificationProvider = ({
	children,
}: {
	children: React.ReactNode
}) => {
	const [notifications, setNotifications] =
		useState<INotifications[]>(initialState)

	useEffect(() => {
		fetchNotifications({ setNotifications: setNotifications })
	}, [])

	return (
		<NotificationContext.Provider value={{ notifications, setNotifications }}>
			{children}
		</NotificationContext.Provider>
	)
}
