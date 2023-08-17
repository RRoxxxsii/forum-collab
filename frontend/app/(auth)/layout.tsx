import { useSession } from 'next-auth/react'
import { redirect } from 'next/navigation'

interface AuthLayoutProps {
	children: React.ReactNode
}

export default function AuthLayout({ children }: AuthLayoutProps) {
	return <div className='min-h-screen min-w-screen'>{children}</div>
}
