'use client'
import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { Alert, AlertTitle } from '@mui/material'
import { useContext } from 'react'

export const EmailAlert = () => {
	const { userDetails } = useContext(UserDetailsContext)

	return userDetails?.email_confirmed ? (
		<Alert variant='outlined' severity='warning' sx={{ mb: 2 }}>
			<AlertTitle>Подтвердите почту</AlertTitle>
			Эта надпись исчезнет, когда вы подтведите свою почту
		</Alert>
	) : null
}
