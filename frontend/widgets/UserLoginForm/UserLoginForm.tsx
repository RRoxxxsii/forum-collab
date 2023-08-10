import { UserLoginSchema, UserLoginType } from '@/lib/UserAuthSchema'
import { zodResolver } from '@hookform/resolvers/zod'
import { Button, FormControl, TextField } from '@mui/material'
import { Controller, useForm } from 'react-hook-form'
export const UserLoginForm = () => {
	const {
		control,
		handleSubmit,
		formState: { errors },
	} = useForm<UserLoginType>({
		mode: 'onChange',
		resolver: zodResolver(UserLoginSchema),
		defaultValues: { email: '', password: '' },
	})

	const onSubmit = (data: UserLoginType) => console.log('click:' + data)

	return (
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
			<Button sx={{ p: 2 }} type='submit'>
				Войти
			</Button>
		</FormControl>
	)
}
