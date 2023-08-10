import { z } from 'zod'

export const UserAuthSchema = z.object({
	username: z.string().trim().min(1, { message: 'Введите имя пользователя' }),
	email: z
		.string()
		.email({ message: 'Почтовый адрес должен включать в себя @' })
		.min(1, { message: 'Введите почтовый адрес' }),
	password: z
		.string()
		.min(6, { message: 'Пароль должен содержать минимум 6 символов' }),
})

export type UserAuthType = z.infer<typeof UserAuthSchema>
