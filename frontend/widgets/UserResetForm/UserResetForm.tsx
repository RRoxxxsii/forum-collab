'use client'
import {
	UserResetSchema,
	UserResetType,
} from '@/lib/validation/auth/UserAuthSchema'
import { zodResolver } from '@hookform/resolvers/zod'
import LoadingButton from '@mui/lab/LoadingButton'
import { FormControl, TextField } from '@mui/material'
import { useRouter } from 'next/navigation'

import { Controller, useForm } from 'react-hook-form'
import { toast } from 'react-toastify'

export const UserResetForm = () => {
	const router = useRouter()

	const {
		control,
		handleSubmit,
		formState: { isLoading },
	} = useForm<UserResetType>({
		mode: 'onChange',
		resolver: zodResolver(UserResetSchema),
		defaultValues: { email: '' },
	})

	async function onSubmit(credentials: UserResetType) {
		const loginToast = toast.loading('Сброс пароля...')
		try {
			const response = await fetch('/api/auth/reset-password', {
				method: 'POST',
				body: JSON.stringify({
					email: credentials.email,
				}),
				headers: { 'Content-Type': 'application/json' },
			})

			const result = await response.json()
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
			router.push('/login')
		} catch (error: any | unknown) {
			toast.update(loginToast, {
				render: 'Соединение с сервером разорвано, попробуйте попытку позже',
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
		}
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
				<LoadingButton
					data-cy='submit-button'
					loading={isLoading}
					variant='outlined'
					sx={{ p: 2 }}
					type='submit'>
					Восстановить
				</LoadingButton>
			</FormControl>
		</>
	)
}
