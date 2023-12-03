'use client'

import { ILinkType } from '@/types'
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'
import MenuIcon from '@mui/icons-material/Menu'
import MuiAppBar, { AppBarProps as MuiAppBarProps } from '@mui/material/AppBar'
import Divider from '@mui/material/Divider'
import Drawer from '@mui/material/Drawer'
import IconButton from '@mui/material/IconButton'
import List from '@mui/material/List'
import { styled } from '@mui/material/styles'
import * as React from 'react'
import { Navlink } from '../Header/Navlink'

interface AppBarProps extends MuiAppBarProps {
	open?: boolean
}

const AppBar = styled(MuiAppBar, {
	shouldForwardProp: (prop) => prop !== 'open',
})<AppBarProps>(({ theme, open }) => ({
	transition: theme.transitions.create(['margin', 'width'], {
		easing: theme.transitions.easing.sharp,
		duration: theme.transitions.duration.leavingScreen,
	}),
	...(open && {
		width: `calc(100% - ${drawerWidth}px)`,
		marginLeft: `${drawerWidth}px`,
		transition: theme.transitions.create(['margin', 'width'], {
			easing: theme.transitions.easing.easeOut,
			duration: theme.transitions.duration.enteringScreen,
		}),
	}),
}))

const drawerWidth = 240

const DrawerHeader = styled('div')(({ theme }) => ({
	display: 'flex',
	alignItems: 'center',
	padding: theme.spacing(0, 1),
	// necessary for content to be below app bar
	...theme.mixins.toolbar,
	justifyContent: 'flex-end',
}))

export const BurgerMenu = ({
	LINKS,
	PUBLIC_USER_LINKS,
	PRIVATE_USER_LINKS,
	session,
}: {
	LINKS: ILinkType[]
	PUBLIC_USER_LINKS: ILinkType[]
	PRIVATE_USER_LINKS: ILinkType[]
	session: boolean
}) => {
	const [open, setOpen] = React.useState(false)

	const handleDrawerOpen = () => {
		setOpen(true)
	}

	const handleDrawerClose = () => {
		setOpen(false)
	}

	return (
		<>
			<Drawer
				sx={{
					width: 0,
					flexShrink: 0,
					'& .MuiDrawer-paper': {
						width: drawerWidth,
						boxSizing: 'border-box',
					},
				}}
				variant='persistent'
				anchor='right'
				open={open}>
				<DrawerHeader>
					<IconButton onClick={handleDrawerClose}>
						<ChevronLeftIcon />
					</IconButton>
				</DrawerHeader>
				<Divider />
				<List>
					{LINKS.map(({ href, icon: Icon, text }) => (
						<Navlink key={href} text={text} href={href} icon={Icon} />
					))}
				</List>
				<Divider />
				<List>
					{session
						? PRIVATE_USER_LINKS.map(({ href, icon: Icon, text }) => (
								<Navlink key={href} text={text} href={href} icon={Icon} />
						  ))
						: PUBLIC_USER_LINKS.map(({ href, icon: Icon, text }) => (
								<Navlink key={href} text={text} href={href} icon={Icon} />
						  ))}
				</List>
			</Drawer>
			<IconButton
				color='inherit'
				aria-label='open drawer'
				onClick={handleDrawerOpen}
				edge='start'
				sx={{ ...(open && { display: 'none' }) }}>
				<MenuIcon />
			</IconButton>
		</>
	)
}
