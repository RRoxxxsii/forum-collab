'use client'
import {
	UserRegisterSchema,
	UserRegisterType,
} from '@/lib/validation/auth/UserAuthSchema'
import { zodResolver } from '@hookform/resolvers/zod'
import LoadingButton from '@mui/lab/LoadingButton'
import { CircularProgress, FormControl, TextField } from '@mui/material'
import { redirect } from 'next/navigation'
import { useRouter } from 'next/navigation'
import { Controller, useForm } from 'react-hook-form'
import { toast } from 'react-toastify'

export const UserRegisterForm = () => {
	const {
		control,
		handleSubmit,
		formState: { errors, isLoading },
	} = useForm<UserRegisterType>({
		mode: 'onChange',
		resolver: zodResolver(UserRegisterSchema),
		defaultValues: { username: '', email: '', password: '' },
	})
	const router = useRouter()

	const registerUser = async (credentials: UserRegisterType) => {
		const { email, password, username } = credentials

		const registerToast = toast.loading('Создание аккаунта...')

		const res = await fetch(`api/auth/register`, {
			method: 'POST',
			body: JSON.stringify({
				email: email,
				password: password,
				user_name: username,
			}),
			headers: { 'Content-Type': 'application/json' },
		})

		const data = await res.json()
		if (!res.ok) {
			toast.update(registerToast, {
				render: data.message,
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
		} else {
			toast.update(registerToast, {
				render: data.message,
				type: 'success',
				isLoading: false,
				autoClose: 3000,
			})
			router.push('/login')
		}
	}

	const onSubmit = (data: UserRegisterType) => {
		registerUser(data)
	}

	if (isLoading) {
		return <CircularProgress />
	}

	return (
		<FormControl
			sx={{ px: 1 }}
			component={'form'}
			onSubmit={handleSubmit(onSubmit)}
			className='w-full'>
			<Controller
				name='email'
				rules={{
					required: true,
				}}
				control={control}
				render={({
					field: { onChange, onBlur, value },
					fieldState: { error },
				}) => (
					<TextField
						label='Почтовый адрес'
						placeholder='example@gmail.com'
						id='email'
						className={`${error && 'border-red-500'}`}
						sx={{ mb: 1, height: 70, WebkitBoxShadow: 'none' }}
						error={!!error}
						helperText={error ? error.message : null}
						onChange={onChange}
						onBlur={onBlur}
						value={value}
					/>
				)}
			/>
			<Controller
				name='username'
				rules={{
					required: true,
				}}
				control={control}
				render={({
					field: { onChange, onBlur, value },
					fieldState: { error },
				}) => (
					<TextField
						label='Имя пользователя'
						autoFocus
						placeholder='username123'
						id='username'
						className={`${error && 'border-red-500'}`}
						sx={{ mb: 1, height: 70, WebkitBoxShadow: 'none' }}
						error={!!error}
						helperText={error ? error.message : null}
						onChange={onChange}
						onBlur={onBlur}
						value={value}
					/>
				)}
			/>
			<Controller
				name='password'
				rules={{
					required: true,
				}}
				control={control}
				render={({
					field: { onChange, onBlur, value },
					fieldState: { error },
				}) => (
					<TextField
						label='Пароль'
						id='password'
						className={error && `border-red-500`}
						sx={{ mb: 2, height: 68 }}
						error={!!error}
						helperText={error ? error.message : null}
						onBlur={onBlur}
						onChange={onChange}
						value={value}
						type='password'
					/>
				)}
			/>
			<LoadingButton
				variant='outlined'
				loading={isLoading}
				sx={{ p: 2 }}
				type='submit'>
				Создать аккаунт
			</LoadingButton>
		</FormControl>
	)
}
