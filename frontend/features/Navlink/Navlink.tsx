'use client'

import { LinkType } from '@/widgets/Header/Header'
import {
	ListItem,
	ListItemButton,
	ListItemIcon,
	ListItemText,
} from '@mui/material'

import Link from 'next/link'

export const Navlink = ({ text, href, icon: Icon }: LinkType) => {
	return (
		//idk how to ts signout
		<ListItem key={text} disablePadding>
			<Link href={href} className='w-full'>
				<ListItemButton>
					<ListItemIcon>
						<Icon />
					</ListItemIcon>
					<ListItemText primary={text} />
				</ListItemButton>
			</Link>
		</ListItem>
	)
}
