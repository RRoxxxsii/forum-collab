import { OauthActions } from '@/features/OauthActions/OauthActions'
import { UserRegisterForm } from '@/widgets/UserRegisterForm'
import { ChevronLeft, LogoDev } from '@mui/icons-material'
import { Metadata } from 'next'
import Link from 'next/link'
import Logo from '@mui/icons-material/NotListedLocation'

export const metadata: Metadata = {
	title: 'Register',
	description: 'Register the account',
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
					<Logo sx={{ width: 32, height: 32, margin: '0 auto' }} />
					<h1 className='text-2xl font-semibold tracking-tight'>
						Создание аккаунта
					</h1>
					<p className='text-sm text-muted-foreground'>
						Введите свое имя пользователя, почтовый адрес и пароль для создания
						аккаунта
					</p>
				</div>
				<UserRegisterForm />
				<p className='px-8 text-center text-sm text-muted-foreground'>
					<Link
						href='/login'
						className='hover:text-brand underline underline-offset-4'>
						Есть аккаунт? Войти
					</Link>
				</p>
				<p className='px-8 text-center text-sm text-muted-foreground text-slate-500'>
					Или же войти с помощью
				</p>
				<OauthActions />
			</div>
		</div>
	)
}
