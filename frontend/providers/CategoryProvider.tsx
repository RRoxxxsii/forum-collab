'use client'
import { CategoryType } from '@/types'
import React, { Dispatch, createContext, useState } from 'react'

const initialState: CategoryType = 'opened'

export const CategoryContext = createContext<{
	category: CategoryType
	setCategory: Dispatch<CategoryType>
}>({
	category: initialState,
	setCategory: () => {},
})

export const CategoryProvider = ({
	children,
}: {
	children: React.ReactNode
}) => {
	const [category, setCategory] = useState<CategoryType>(initialState)

	return (
		<CategoryContext.Provider value={{ category, setCategory }}>
			{children}
		</CategoryContext.Provider>
	)
}
