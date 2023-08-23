import { ChevronLeft, LogoDev } from '@mui/icons-material'
import { Metadata } from 'next'
import { UserResetForm } from '@/widgets/UserResetForm'
import Link from 'next/link'

export const metadata: Metadata = {
	title: 'Reset password',
	description: "Reset account's password",
}

export default function RegisterPage() {
	return (
		<div className=' flex h-screen w-screen flex-col items-center justify-center relative'>
			<Link className='absolute top-4 left-4' href='/'>
				<>
					<ChevronLeft className='mr-2 h-4 w-4' />
					Back
				</>
			</Link>
			<div className='mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]'>
				<div className='flex flex-col space-y-2 text-center'>
					<LogoDev className='mx-auto h-6 w-6' />
					<h1 className='text-2xl font-semibold tracking-tight'>
						Восстановление аккаунта
					</h1>
					<p className='text-sm text-muted-foreground'>
						Введите свое почтовый адрес, чтобы получить на него дальнейшие
						инструкции
					</p>
				</div>
				<UserResetForm />
			</div>
		</div>
	)
}
