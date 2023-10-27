'use client'
import { fetchMe } from '@/shared/api/fetchData'
import { IUser, UserDetailsType } from '@/types'
import React, {
	Dispatch,
	SetStateAction,
	createContext,
	useEffect,
	useState,
} from 'react'

const initialState: UserDetailsType = null

interface UserDetailsProviderProps {
	userDetails: UserDetailsType
	setUserDetails: Dispatch<SetStateAction<IUser | null>>
}

export const UserDetailsContext = createContext<UserDetailsProviderProps>({
	userDetails: initialState,
	setUserDetails: () => {},
})

export const UserDetailsProvider = ({
	children,
}: {
	children: React.ReactNode
}) => {
	const [userDetails, setUserDetails] = useState<UserDetailsType>(initialState)

	useEffect(() => {
		fetchMe({ setProfileData: setUserDetails })
	}, [])

	return (
		<UserDetailsContext.Provider value={{ userDetails, setUserDetails }}>
			{children}
		</UserDetailsContext.Provider>
	)
}
