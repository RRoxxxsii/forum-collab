import { AskFastProvider } from '@/providers/AskFastProvider'
import { CategoryProvider } from '@/providers/CategoryProvider'
import { Header } from '@/widgets/Header'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

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
			<Header>
				<CategoryProvider>
					<AskFastProvider>{children}</AskFastProvider>
				</CategoryProvider>
			</Header>
		</>
	)
}
