'use client'
import React, { Dispatch, createContext, useState } from 'react'

export const AskFastContext = createContext<{
	askFastValue: string
	setAskFastValue: Dispatch<string>
}>({
	askFastValue: '',
	setAskFastValue: () => {},
})

export const AskFastProvider = ({
	children,
}: {
	children: React.ReactNode
}) => {
	const [askFastValue, setAskFastValue] = useState<string>('')

	return (
		<AskFastContext.Provider value={{ askFastValue, setAskFastValue }}>
			{children}
		</AskFastContext.Provider>
	)
}
