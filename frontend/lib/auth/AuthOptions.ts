import { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'
import GitHubProvider from 'next-auth/providers/github'
import GoogleProvider from 'next-auth/providers/google'

import { toast } from 'react-toastify'
import { UserLoginSchema } from '../validation/auth/UserAuthSchema'

export const authOptions: NextAuthOptions = {
	session: {
		strategy: 'jwt',
	},
	providers: [
		GitHubProvider({
			clientId: process.env.GITHUB_CLIENT_ID ?? '',
			clientSecret: process.env.GITHUB_CLIENT_SECRET ?? '',
		}),
		GoogleProvider({
			clientId: process.env.GOOGLE_CLIENT_ID ?? '',
			clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? '',
		}),
		CredentialsProvider({
			name: 'Credentials',
			credentials: {
				email: { label: 'Email', type: 'email' },
				password: { label: 'Password', type: 'password' },
			},
			async authorize(credentials, req) {
				const { email, password } = UserLoginSchema.parse(credentials)

				const loginToast = toast.loading('Авторизация...')

				const response = await fetch(
					'http://localhost:8000/api/v1/account/token/',
					{
						method: 'POST',
						body: JSON.stringify({ email, password }),
						headers: {
							'Content-Type': 'application/json',
						},
					}
				)

				const user = await response.json()

				if (!response.ok) {
					toast.update(loginToast, {
						render: 'Что-то пошло не так, попробуйте снова',
						autoClose: 4000,
						type: 'error',
						isLoading: false,
					})
				}
				// If no error and we have user data, return it
				if (response.ok && user) {
					toast.update(loginToast, {
						render: 'Вы успешно авторизовались',
						autoClose: 4000,
						type: 'success',
						isLoading: false,
					})
					return user
				}
				// Return null if user data could not be retrieved
				return null
			},
		}),
	],
	callbacks: {
		async jwt({ token, account }) {
			// Persist the OAuth access_token to the token right after signin
			if (account) {
				token.accessToken = account.access_token
			}
			return token
		},
	},
	pages: {
		signIn: '/login',
	},
}
