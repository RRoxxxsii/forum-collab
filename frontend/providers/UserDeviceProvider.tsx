'use client'
import { useMediaQuery } from '@/lib/hooks/useMediaQuery'
import React, { createContext, useEffect, useState } from 'react'

interface UserDeviceProviderProps {
	userDevice: 'desktop' | 'mobile'
}

export const UserDeviceContext = createContext<UserDeviceProviderProps>({
	userDevice: 'desktop',
})

export const UserDeviceProvider = ({
	children,
}: {
	children: React.ReactNode
}) => {
	const [userDevice, setUserDevice] = useState<'desktop' | 'mobile'>('desktop')
	const desktop = useMediaQuery('(min-width: 768px)')

	useEffect(() => {
		if (desktop) {
			setUserDevice('desktop')
		} else {
			setUserDevice('mobile')
		}
	})

	return (
		<UserDeviceContext.Provider value={{ userDevice }}>
			{children}
		</UserDeviceContext.Provider>
	)
}
