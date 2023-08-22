import { Navlink } from '@/features/Navlink'
import { Login } from '@mui/icons-material'
import DashboardIcon from '@mui/icons-material/Dashboard'
import HomeIcon from '@mui/icons-material/Home'
import LiveHelpIcon from '@mui/icons-material/LiveHelp'
import LogoutIcon from '@mui/icons-material/Logout'
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer'
import SettingsIcon from '@mui/icons-material/Settings'
import SupportIcon from '@mui/icons-material/Support'
import AccountBoxIcon from '@mui/icons-material/AccountBox'

import {
	AppBar,
	Box,
	Divider,
	Drawer,
	List,
	ListItem,
	ListItemButton,
	ListItemIcon,
	ListItemText,
	SvgIconProps,
	SvgIconTypeMap,
	Toolbar,
	Typography,
} from '@mui/material'
import { OverridableComponent } from '@mui/material/OverridableComponent'
import { cookies } from 'next/headers'
import Link from 'next/link'
import { ReactElement, JSXElementConstructor, ElementType } from 'react'

export const metadata = {
	title: 'Header',
	description: 'Navbar',
}

const DRAWER_WIDTH = 240

export interface LinkType {
	text: string
	href: string
	//YO WTF IS THIS DEMON TYPE?
	icon:
		| ReactElement<SvgIconProps, string | JSXElementConstructor<any>>
		| (OverridableComponent<SvgIconTypeMap<{}, 'svg'>> & {
				muiName: string
		  })
		| ElementType
}

const LINKS: LinkType[] = [
	{ text: 'Главная', href: '/', icon: HomeIcon },
	{ text: 'Вопросы', href: '/questions', icon: QuestionAnswerIcon },
	{ text: 'Спросить', href: '/ask', icon: LiveHelpIcon },
]

const PUBLIC_USER_LINKS: LinkType[] = [
	{ text: 'Настройки', icon: SettingsIcon, href: '/settings' },
	{ text: 'Поддержка', icon: SupportIcon, href: '/support' },
	{ text: 'Войти', icon: Login, href: '/login' },
]

const PRIVATE_USER_LINKS: LinkType[] = [
	{ text: 'Настройки', icon: SettingsIcon, href: '/settings' },
	{ text: 'Поддержка', icon: SupportIcon, href: '/support' },
	{
		text: 'Профиль',
		icon: AccountBoxIcon,
		href: '/profile',
	},
]

export const Header = async ({ children }: { children: React.ReactNode }) => {
	const session = cookies().has('access_token')

	return (
		<>
			<header>
				<AppBar position='fixed' sx={{ zIndex: 2000 }}>
					<Toolbar sx={{ backgroundColor: 'background.paper' }}>
						<DashboardIcon
							sx={{ color: '#444', mr: 2, transform: 'translateY(-2px)' }}
						/>
						<Typography variant='h6' noWrap component='div'>
							Вопрос-Ответ
						</Typography>
					</Toolbar>
				</AppBar>

				<Drawer
					sx={{
						width: DRAWER_WIDTH,
						flexShrink: 0,
						'& .MuiDrawer-paper': {
							width: DRAWER_WIDTH,
							boxSizing: 'border-box',
							top: ['48px', '56px', '64px'],
							height: 'auto',
							bottom: 0,
						},
					}}
					variant='permanent'
					anchor='left'>
					<Divider />
					<List>
						{LINKS.map(({ text, href, icon: Icon }) => (
							<Navlink key={href} text={text} href={href} icon={Icon} />
						))}
					</List>
					<Divider sx={{ mt: 'auto' }} />
					<List>
						{session
							? PRIVATE_USER_LINKS.map(({ text, icon: Icon, href }) => (
									<Navlink key={href} text={text} href={href} icon={Icon} />
							  ))
							: PUBLIC_USER_LINKS.map(({ text, icon: Icon, href }) => (
									<Navlink key={href} text={text} href={href} icon={Icon} />
							  ))}
					</List>
				</Drawer>
			</header>
			<Box
				component='main'
				sx={{
					flexGrow: 1,
					bgcolor: 'background.default',
					ml: `${DRAWER_WIDTH}px`,
					mt: ['48px', '56px', '64px'],
					p: 3,
				}}>
				{children}
			</Box>
		</>
	)
}
