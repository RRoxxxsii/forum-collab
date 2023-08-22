'use client'
import {
	UserLoginSchema,
	UserLoginType,
} from '@/lib/validation/auth/UserAuthSchema'
import { zodResolver } from '@hookform/resolvers/zod'
import LoadingButton from '@mui/lab/LoadingButton'
import { FormControl, TextField } from '@mui/material'
import { useRouter } from 'next/navigation'

import { Controller, useForm } from 'react-hook-form'
import { toast } from 'react-toastify'

export const UserLoginForm = () => {
	const router = useRouter()

	const {
		control,
		handleSubmit,
		formState: { errors, isLoading },
	} = useForm<UserLoginType>({
		mode: 'onChange',
		resolver: zodResolver(UserLoginSchema),
		defaultValues: { email: '', password: '' },
	})

	async function onSubmit(credentials: UserLoginType) {
		const loginToast = toast.loading('Авторизация...')
		const response = await fetch('/api/auth/login', {
			method: 'POST',
			body: JSON.stringify({
				email: credentials.email,
				password: credentials.password,
			}),
			headers: { 'Content-Type': 'application/json' },
		})

		const result = await response.json()
		console.log(result)
		if (!response.ok) {
			toast.update(loginToast, {
				render: result.detail,
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
			return null
		}
		toast.update(loginToast, {
			render: result.message,
			type: 'success',
			isLoading: false,
			autoClose: 3000,
		})
		router.push('/')
	}

	return (
		<>
			<FormControl component={'form'} onSubmit={handleSubmit(onSubmit)}>
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
							data-cy='email'
							label='Почтовый адрес'
							autoFocus
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
							data-cy='password'
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
					data-cy='submit-button'
					loading={isLoading}
					variant='outlined'
					sx={{ p: 2 }}
					type='submit'>
					Войти
				</LoadingButton>
			</FormControl>
		</>
	)
}
