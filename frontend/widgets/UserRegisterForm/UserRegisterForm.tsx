'use client'
import {
	UserRegisterSchema,
	UserRegisterType,
} from '@/lib/validation/auth/UserAuthSchema'
import { zodResolver } from '@hookform/resolvers/zod'
import LoadingButton from '@mui/lab/LoadingButton'
import { CircularProgress, FormControl, TextField } from '@mui/material'
import axios from 'axios'
import { NextResponse } from 'next/server'
import { Controller, useForm } from 'react-hook-form'

export const registerUser = async (credentials: UserRegisterType) => {
	const { email, password, username } = credentials
	try {
		const res = await axios(
			'http://localhost:8000/api/v1/account/create-account/',
			{
				method: 'POST',
				data: JSON.stringify({
					email: email,
					user_name: username,
					password: password,
				}),
				headers: {
					'Content-Type': 'application/json',
				},
			}
		)
		if (!res.data) {
			console.log(res)
		}
	} catch (error) {
		console.log(error)
	}
	return NextResponse.json
}

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

	const onSubmit = (data: UserRegisterType) => {
		registerUser(data)
	}

	if (isLoading) {
		return <CircularProgress />
	}

	return (
		<FormControl
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
						placeholder='example@gmail.com'
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
