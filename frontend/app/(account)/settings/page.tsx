import { AccountDeletion } from '@/components/settings/AccountDeletion'
import { OauthActions } from '@/features/OauthActions/OauthActions'
import { ChevronLeft, Settings } from '@mui/icons-material'
import Logo from '@mui/icons-material/NotListedLocation'
import { Button } from '@mui/material'
import { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
	title: 'Settings',
	description: 'Configure your account',
}

export default function SettingsPage() {
	return (
		<div className=' flex h-screen w-screen flex-col items-center justify-center relative'>
			<Link data-cy='home-link' className='absolute top-4 left-4' href='/'>
				<>
					<ChevronLeft className='mr-2 h-4 w-4' />
					Back
				</>
			</Link>
			<div className='mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]'>
				<div className='flex flex-col space-y-2 text-center justify-center items-center'>
					<Settings sx={{ width: 32, height: 32, margin: '0 auto' }} />
					<h1 className='text-2xl font-semibold tracking-tight mb-12'>
						Настройки
					</h1>
					<AccountDeletion />
				</div>
			</div>
		</div>
	)
}
