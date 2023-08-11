'use client'

import { UserLoginForm } from '@/widgets/UserLoginForm'
import { ChevronLeft, LogoDev } from '@mui/icons-material'
import { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
	title: 'Login',
	description: 'Login to your account',
}

export default function LoginPage() {
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
						И снова здравствуйте
					</h1>
					<p className='text-sm text-muted-foreground'>
						Введите свой почтовый адрес и пароль для входа в аккаунт
					</p>
				</div>
				<UserLoginForm />
				<p className='px-8 text-center text-sm text-muted-foreground'>
					<Link
						data-cy='register-link'
						href='/register'
						className='hover:text-brand underline underline-offset-4'>
						Нет аккаунта? Зарегистрироваться
					</Link>
				</p>
			</div>
		</div>
	)
}
