'use client'
import {
	UserLoginSchema,
	UserLoginType,
} from '@/lib/validation/auth/UserAuthSchema'
import { zodResolver } from '@hookform/resolvers/zod'
import LoadingButton from '@mui/lab/LoadingButton'
import { FormControl, TextField } from '@mui/material'
import cookie from 'js-cookie'
import { redirect } from 'next/navigation'
import { Controller, useForm } from 'react-hook-form'
import { toast } from 'react-toastify'

export const LoginUser = async (credentials: UserLoginType) => {
	const { email, password } = credentials

	const loginToast = toast.loading('Авторизация...')
	try {
		const res = await fetch('http://localhost:8000/api/v1/account/token/', {
			method: 'POST',
			body: JSON.stringify({
				email: email,
				password: password,
			}),
			headers: {
				'Content-Type': 'application/json',
			},
		})

		if (!res.ok) {
			console.log(res)
			toast.update(loginToast, {
				render: 'Неправильный почтовый адрес или пароль',
				type: 'error',
				isLoading: false,
			})
			return
		}
		const { access, refresh } = await res.json()

		toast.update(loginToast, {
			render: 'Вы успешно авторизовались!',
			type: 'success',
			isLoading: false,
		})

		cookie.set('access_token', access, { expires: 86400 }) // Сохраняем access токен в куках
		cookie.set('refresh_token', refresh, { expires: 30 }) // Сохраняем refresh токен в куках
		redirect('/')
	} catch (error) {
		console.log(error)
	}
}

export const UserLoginForm = () => {
	const {
		control,
		handleSubmit,
		formState: { errors, isLoading },
	} = useForm<UserLoginType>({
		mode: 'onChange',
		resolver: zodResolver(UserLoginSchema),
		defaultValues: { email: '', password: '' },
	})

	const onSubmit = (data: UserLoginType) => {
		LoginUser(data)
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
