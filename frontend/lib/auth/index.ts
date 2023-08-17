import { NextAuthOptions } from 'next-auth'
import CredentialsProvider from 'next-auth/providers/credentials'

export const authOptions: NextAuthOptions = {
	session: {
		strategy: 'jwt',
	},

	providers: [
		CredentialsProvider({
			name: 'Credentials',
			credentials: {
				email: { label: 'Email', type: 'email' },
				password: { label: 'Password', type: 'password' },
			},
			async authorize(credentials, req) {
				const payload = {
					email: credentials?.email,
					password: credentials?.password,
				}
				const res = await fetch('https://localhost:8080/api/tokens', {
					method: 'POST',
					body: JSON.stringify(payload),
					headers: {
						'Content-Type': 'application/json',
					},
				})
				const user = await res.json()
				if (!res.ok) {
					throw new Error(user.message)
				}
				// If no error and we have user data, return it
				if (res.ok && user) {
					return user
				}

				// Return null if user data could not be retrieved
				return null
			},
		}),
	],
	pages: {
		signIn: '/login',
	},
	callbacks: {
		// async jwt({ token, user, account }) {
		// 	if (account && user) {
		// 		return {
		// 			...token,
		// 			accessToken: user.token,
		// 			refreshToken: user.refreshToken,
		// 		}
		// 	}
		// 	return token
		// },
		// async session({ session, token }) {
		// 	session.user.accessToken = token.accessToken
		// 	session.user.refreshToken = token.refreshToken
		// 	session.user.accessTokenExpires = token.accessTokenExpires
		// 	return session
		// },
	},
}

//TODO: GOOGLE AND GIT OAUTH
// GoogleProvider({
// 	clientId: process.env.GOOGLE_CLIENT_ID ?? '',
// 	clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? '',
// 	allowDangerousEmailAccountLinking: true,
// 	profile(profile) {
// 		return {
// 			id: profile.id,
// 			email: profile.email,
// 			name: profile.name,
// 			image: profile.image,
// 		}
// 	},
// }),
// GitHubProvider({
// 	clientId: process.env.GITHUB_CLIENT_ID ?? '',
// 	clientSecret: process.env.GITHUB_CLIENT_SECRET ?? '',
// }),
