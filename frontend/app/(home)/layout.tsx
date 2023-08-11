import { Header } from '@/widgets/Header'

interface HomeLayoutProps {
	children: React.ReactNode
}

export default async function HomeLayout({ children }: HomeLayoutProps) {
	return (
		<div className=''>
			<Header>{children}</Header>
		</div>
	)
}
