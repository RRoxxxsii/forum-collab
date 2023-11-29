import { Metadata } from 'next'

interface QuestionsLayoutProps {
	children: React.ReactNode
}
export const metadata: Metadata = {
	title: 'Вопросы',
	description: 'Список вопросов',
}

export default async function QuestionsLayout({
	children,
}: QuestionsLayoutProps) {
	return <div className=''>{children}</div>
}
