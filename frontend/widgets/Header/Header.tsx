import { Login } from '@mui/icons-material'
import DashboardIcon from '@mui/icons-material/Dashboard'
import HomeIcon from '@mui/icons-material/Home'
import LiveHelpIcon from '@mui/icons-material/LiveHelp'
import LogoutIcon from '@mui/icons-material/Logout'
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer'
import SettingsIcon from '@mui/icons-material/Settings'
import SupportIcon from '@mui/icons-material/Support'
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
	Toolbar,
	Typography,
} from '@mui/material'
import Link from 'next/link'

export const metadata = {
	title: 'Header',
	description: 'Navbar',
}

const DRAWER_WIDTH = 240

const LINKS = [
	{ text: 'Главная', href: '/', icon: HomeIcon },
	{ text: 'Вопросы', href: '/questions', icon: QuestionAnswerIcon },
	{ text: 'Спросить', href: '/ask', icon: LiveHelpIcon },
]

const PUBLIC_USER_LINKS = [
	{ text: 'Настройки', icon: SettingsIcon, href: '/settings' },
	{ text: 'Поддержка', icon: SupportIcon, href: '/support' },
	{ text: 'Войти', icon: Login, href: '/login' },
]

const PRIVATE_USER_LINKS = [
	{ text: 'Settings', icon: SettingsIcon },
	{ text: 'Support', icon: SupportIcon },
	{ text: 'Logout', icon: LogoutIcon },
]

export const Header = ({ children }: { children: React.ReactNode }) => {
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
							<ListItem key={href} disablePadding>
								<Link href={href} className='w-full'>
									<ListItemButton>
										<ListItemIcon>
											<Icon />
										</ListItemIcon>
										<ListItemText primary={text} />
									</ListItemButton>
								</Link>
							</ListItem>
						))}
					</List>
					<Divider sx={{ mt: 'auto' }} />
					<List>
						{PUBLIC_USER_LINKS.map(({ text, icon: Icon, href }) => (
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
