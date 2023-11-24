'use client'

import {
	ListItem,
	ListItemButton,
	ListItemIcon,
	ListItemText,
} from '@mui/material'

import { Logout as LogoutIcon } from '@mui/icons-material'
import { useRouter } from 'next/navigation'

export const Logout = () => {
	const router = useRouter()

	const LogoutAction = async () => {
		try {
			const response = await fetch('/api/auth/logout', { method: 'GET' })
			const result = await response.json()
			if (!response.ok) {
				throw new Error(result)
			}
			router.refresh()
			return { ...result }
		} catch (error) {
			if (typeof error === 'string') {
				return error
			}
			if (error instanceof Error) {
				return error.message
			}
		}
	}

	return (
		<ListItem disablePadding>
			<ListItemButton onClick={LogoutAction}>
				<ListItemIcon>
					<LogoutIcon />
				</ListItemIcon>
				<ListItemText primary={'Выйти'} />
			</ListItemButton>
		</ListItem>
	)
}
