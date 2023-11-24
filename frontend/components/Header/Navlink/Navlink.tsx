'use client'

import { NotificationContext } from '@/providers/NotificationsProvider'
import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { ILinkType } from '@/types'
import {
	Badge,
	ListItem,
	ListItemButton,
	ListItemIcon,
	ListItemText,
} from '@mui/material'

import Link from 'next/link'
import { useContext } from 'react'
import { toast } from 'react-toastify'

export const Navlink = ({ text, href, icon: Icon, session }: ILinkType) => {
	const { notifications } = useContext(NotificationContext)
	const { userDetails } = useContext(UserDetailsContext)

	const profileHandler = () => {
		if (!userDetails) {
			toast.error('Вам необходимо авторизоваться')
		}
		if (!userDetails) {
			toast.error('Вам необходимо авторизоваться')
		}
	}

	const settingsHandler = () => {
		if (!userDetails) {
			toast.error('Вам необходимо авторизоваться')
		}
		if (!userDetails) {
			toast.error('Вам необходимо авторизоваться')
		}
	}

	const IconManager = () => {
		if (text === 'Уведомления') {
			return (
				<ListItemButton>
					<ListItemIcon>
						<Badge
							badgeContent={session && notifications ? notifications.length : 0}
							color='primary'>
							<Icon />
						</Badge>
					</ListItemIcon>
					<ListItemText primary={text} />
				</ListItemButton>
			)
		}

		if (text === 'Профиль') {
			return (
				<ListItemButton onClick={profileHandler}>
					<ListItemIcon>
						<Icon />
					</ListItemIcon>
					<ListItemText primary={text} />
				</ListItemButton>
			)
		}

		if (text === 'Настройки') {
			return (
				<ListItemButton onClick={settingsHandler}>
					<ListItemIcon>
						<Icon />
					</ListItemIcon>
					<ListItemText primary={text} />
				</ListItemButton>
			)
		}

		return (
			<ListItemButton>
				<ListItemIcon>
					<Icon />
				</ListItemIcon>
				<ListItemText primary={text} />
			</ListItemButton>
		)
	}

	return (
		//idk how to ts signout
		<ListItem key={text} disablePadding>
			<Link href={href} className='w-full'>
				<IconManager />
			</Link>
		</ListItem>
	)
}
