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

export const Navlink = ({
	text,
	href,
	icon: Icon,
	action,
	session,
}: ILinkType) => {
	const { notifications } = useContext(NotificationContext)
	const { userDetails } = useContext(UserDetailsContext)

	return (
		//idk how to ts signout
		<ListItem key={text} disablePadding>
			<Link href={href} className='w-full'>
				<ListItemButton action={action}>
					<ListItemIcon>
						{text === 'Уведомления' ? (
							<Badge
								badgeContent={
									session && notifications ? notifications.length : 0
								}
								color='primary'>
								<Icon />
							</Badge>
						) : (
							<Icon />
						)}
					</ListItemIcon>
					<ListItemText primary={text} />
				</ListItemButton>
			</Link>
		</ListItem>
	)
}
