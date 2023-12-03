import { Header } from '@/components/Header'
import { AskFastProvider } from '@/providers/AskFastProvider'
import { CategoryProvider } from '@/providers/CategoryProvider'
import { NotificationProvider } from '@/providers/NotificationsProvider'
import { UserDetailsProvider } from '@/providers/UserDetailsProvider'
import { UserDeviceProvider } from '@/providers/UserDeviceProvider'
import { Metadata } from 'next'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

export const metadata: Metadata = {
	title: 'Yoman',
	description: 'Форум для решения вопросов всех областей и направлений',
}

interface HomeLayoutProps {
	children: React.ReactNode
}

export default function HomeLayout({ children }: HomeLayoutProps) {
	return (
		<>
			<ToastContainer
				position='bottom-center'
				autoClose={5000}
				hideProgressBar={false}
				newestOnTop={false}
				closeOnClick
				rtl={false}
				pauseOnFocusLoss={false}
				draggable
				pauseOnHover
				theme='dark'
				limit={5}
			/>
			<UserDeviceProvider>
				<UserDetailsProvider>
					<NotificationProvider>
						<Header>
							<CategoryProvider>
								<AskFastProvider>{children}</AskFastProvider>
							</CategoryProvider>
						</Header>
					</NotificationProvider>
				</UserDetailsProvider>
			</UserDeviceProvider>
		</>
	)
}
