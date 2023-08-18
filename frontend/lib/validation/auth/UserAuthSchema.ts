import { z } from 'zod'

export const UserRegisterSchema = z.object({
	username: z.string().trim().min(1, { message: 'Введите имя пользователя' }),
	email: z
		.string()
		.email({ message: 'Неправильный формат почтового адреса' })
		.min(1, { message: 'Введите почтовый адрес' }),
	password: z
		.string()
		.min(6, { message: 'Пароль должен содержать минимум 6 символов' })
		.refine((value: string) => !/^\d+$/.test(value), {
			message: 'Пароль не может состоять только из цифр',
		}),
})

export type UserRegisterType = z.infer<typeof UserRegisterSchema>

export const UserLoginSchema = z.object({
	email: z
		.string()
		.email({ message: 'Неправильный формат почтового адреса' })
		.min(1, { message: 'Введите почтовый адрес' }),
	password: z
		.string()
		.min(6, { message: 'Пароль должен содержать минимум 6 символов' }),
})

export type UserLoginType = z.infer<typeof UserLoginSchema>
