import { Header } from '@/widgets/Header'

interface QuestionsLayoutProps {
	children: React.ReactNode
}

export default async function QuestionsLayout({
	children,
}: QuestionsLayoutProps) {
	return (
		<div className=''>
			<Header>{children}</Header>
		</div>
	)
}
