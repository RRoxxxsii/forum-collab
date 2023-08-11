import NextAuth from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import GitHubProvider from 'next-auth/providers/github'

const secret = process.env.NEXTAUTH_SECRET

const handler = NextAuth({
	session: {
		strategy: 'jwt',
	},
	pages: {
		signIn: '/login',
	},
	providers: [
		GoogleProvider({
			clientId: process.env.GOOGLE_CLIENT_ID ?? '',
			clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? '',
			allowDangerousEmailAccountLinking: true,
			profile(profile) {
				return {
					id: profile.id,
					email: profile.email,
					name: profile.name,
					image: profile.image,
				}
			},
		}),
		GitHubProvider({
			clientId: process.env.GITHUB_CLIENT_ID ?? '',
			clientSecret: process.env.GITHUB_CLIENT_SECRET ?? '',
		}),
	],
	callbacks: {
		// async session({ token, session }) {
		// 	if (token) {
		// 		session.user.id = token.id
		// 		session.user.name = token.name
		// 		session.user.email = token.email
		// 		session.user.image = token.picture
		// 	}
		// 	return session
		// },
		// async jwt({ token, user }) {
		// 	const dbUser = await db.user.findFirst({
		// 		where: {
		// 			email: token.email,
		// 		},
		// 	})
		// 	if (!dbUser) {
		// 		if (user) {
		// 			token.id = user?.id
		// 		}
		// 		return token
		// 	}
		// 	return {
		// 		id: dbUser.id,
		// 		name: dbUser.name,
		// 		email: dbUser.email,
		// 		picture: dbUser.image,
		// 	}
		// },
	},
})

export { handler as GET, handler as POST }
