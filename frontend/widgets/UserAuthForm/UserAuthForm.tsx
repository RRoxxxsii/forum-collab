import { UserAuthSchema, UserAuthType } from '@/lib/UserAuthSchema'
import { zodResolver } from '@hookform/resolvers/zod'
import { SubmitHandler, useForm } from 'react-hook-form'

export const UserAuthForm = () => {
	const {
		register,
		handleSubmit,
		formState: { errors },
	} = useForm<UserAuthType>({ resolver: zodResolver(UserAuthSchema) })

	const onSubmit: SubmitHandler<UserAuthType> = (data) => console.log(data)

	return (
		<form className='px-8 pt-6 pb-8 mb-4' onSubmit={handleSubmit(onSubmit)}>
			<div className='mb-4 md:flex md:justify-between'>
				<div className='mb-4 md:mr-2 md:mb-0'>
					<label
						className='block mb-2 text-sm font-bold text-gray-700'
						htmlFor='firstName'>
						Имя пользователя
					</label>
					<input
						className={`w-full px-3 py-2 text-sm leading-tight text-gray-700 border ${
							errors.username && 'border-red-500'
						} rounded appearance-none focus:outline-none focus:shadow-outline`}
						id='firstName'
						type='text'
						placeholder='First Name'
						{...register('username')}
					/>
					{errors.username && (
						<p className='text-xs italic text-red-500 mt-2'>
							{errors.username?.message}
						</p>
					)}
				</div>
			</div>
			<div className='mb-4'>
				<label
					className='block mb-2 text-sm font-bold text-gray-700'
					htmlFor='email'>
					Email
				</label>
				<input
					className={`w-full px-3 py-2 text-sm leading-tight text-gray-700 border ${
						errors.email && 'border-red-500'
					} rounded appearance-none focus:outline-none focus:shadow-outline`}
					id='email'
					type='email'
					placeholder='Email'
					{...register('email')}
				/>
				{errors.email && (
					<p className='text-xs italic text-red-500 mt-2'>
						{errors.email?.message}
					</p>
				)}
			</div>
			<div className='mb-4 md:flex md:justify-between'>
				<div className='mb-4 md:mr-2 md:mb-0'>
					<label
						className='block mb-2 text-sm font-bold text-gray-700'
						htmlFor='password'>
						Password
					</label>
					<input
						className={`w-full px-3 py-2 text-sm leading-tight text-gray-700 border ${
							errors.password && 'border-red-500'
						} rounded appearance-none focus:outline-none focus:shadow-outline`}
						id='password'
						type='password'
						{...register('password')}
					/>
					{errors.password && (
						<p className='text-xs italic text-red-500 mt-2'>
							{errors.password?.message}
						</p>
					)}
				</div>
			</div>
			<div className='mb-6 text-center'>
				<button
					className='w-full px-4 py-2 font-bold text-white bg-blue-500 rounded-full hover:bg-blue-700 focus:outline-none focus:shadow-outline'
					type='submit'>
					Register Account
				</button>
			</div>
			<hr className='mb-6 border-t' />
			<div className='text-center'>
				<a
					className='inline-block text-sm text-blue-500 align-baseline hover:text-blue-800'
					href='#test'>
					Forgot Password?
				</a>
			</div>
			<div className='text-center'>
				<a
					className='inline-block text-sm text-blue-500 align-baseline hover:text-blue-800'
					href='./index.html'>
					Already have an account? Login!
				</a>
			</div>
		</form>
	)
}
