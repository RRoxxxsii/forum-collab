import { BurgerMenu } from '@/features/BurgerMenu'
import { Navlink } from '@/features/Navlink'
import { LinkType } from '@/types/types'
import { Login } from '@mui/icons-material'
import AccountBoxIcon from '@mui/icons-material/AccountBox'
import HomeIcon from '@mui/icons-material/Home'
import LiveHelpIcon from '@mui/icons-material/LiveHelp'
import Logo from '@mui/icons-material/NotListedLocation'
import NotificationsIcon from '@mui/icons-material/Notifications'
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer'
import SettingsIcon from '@mui/icons-material/Settings'
import {
	AppBar,
	Box,
	Divider,
	Drawer,
	List,
	Toolbar,
	Typography,
} from '@mui/material'
import { cookies } from 'next/headers'
import './styles.scss'

export const metadata = {
	title: 'Header',
	description: 'Navbar',
}

const DRAWER_WIDTH = 240

const LINKS: LinkType[] = [
	{ text: 'Главная', href: '/', icon: HomeIcon },
	{ text: 'Вопросы', href: '/questions', icon: QuestionAnswerIcon },
	{ text: 'Спросить', href: '/ask', icon: LiveHelpIcon },
]

const PUBLIC_USER_LINKS: LinkType[] = [
	{ text: 'Настройки', icon: SettingsIcon, href: '/settings' },
	{ text: 'Уведомления', icon: NotificationsIcon, href: '/notifications' },
	{ text: 'Войти', icon: Login, href: '/login' },
]

const PRIVATE_USER_LINKS: LinkType[] = [
	{ text: 'Настройки', icon: SettingsIcon, href: '/settings' },
	{ text: 'Уведомления', icon: NotificationsIcon, href: '/notifications' },
	{
		text: 'Профиль',
		icon: AccountBoxIcon,
		href: '/profile',
	},
]

const burgerMenu = {
	display: { md: 'none', xs: 'block' },
}

export const Header = ({ children }: { children: React.ReactNode }) => {
	return (
		<>
			<HeaderDesktop>{children}</HeaderDesktop>
		</>
	)
}

export const HeaderDesktop = async ({
	children,
}: {
	children: React.ReactNode
}) => {
	const session = cookies().has('refresh_token')

	return (
		<>
			<header className='header-desktop'>
				<AppBar position='fixed' sx={{ zIndex: 2000 }}>
					<Toolbar
						sx={{
							backgroundColor: 'background.paper',
							display: 'flex',
							justifyContent: 'space-between',
						}}>
						<Box sx={{ display: 'flex', alignItems: 'center' }}>
							<Logo sx={{ mr: 1, width: 32, height: 32 }} />
							<Typography variant='h6' noWrap component='div'>
								Yoman
							</Typography>
						</Box>
						<Box sx={burgerMenu}>
							<BurgerMenu
								session={session}
								LINKS={LINKS}
								PRIVATE_USER_LINKS={PRIVATE_USER_LINKS}
								PUBLIC_USER_LINKS={PUBLIC_USER_LINKS}
							/>
						</Box>
					</Toolbar>
				</AppBar>

				<Drawer
					className='drawer'
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
				className='main'
				component='main'
				sx={{
					flexGrow: 1,
					bgcolor: 'background.default',
					ml: `${DRAWER_WIDTH}px`,
					mt: ['48px', '56px', '64px'],
					p: 'md:3',
				}}>
				{children}
			</Box>
		</>
	)
}
