import ThemeRegistry from '@/shared/theme/ThemeRegistry'
import '@fontsource/roboto/300.css'
import '@fontsource/roboto/400.css'
import '@fontsource/roboto/500.css'
import '@fontsource/roboto/700.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.scss'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
	title: 'yoman',
	description: 'Русский форум для решения задач всех областей',
}

export default function RootLayout({
	children,
}: {
	children: React.ReactNode
}) {
	return (
		<html lang='en'>
			<head />
			<body className={inter.className}>
				<ThemeRegistry>{children}</ThemeRegistry>
			</body>
		</html>
	)
}
