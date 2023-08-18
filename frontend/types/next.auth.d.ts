import NextAuth from 'next-auth'

declare module 'next-auth' {
	/**
	 * Returned by `useSession`, `getSession` and received as
	 * a prop on the `SessionProvider` React Context
	 */
	interface Session {
		refreshTokenExpires?: number
		accessTokenExpires?: string
		refreshToken?: string
		token?: string
		error?: string
		user?: User
	}

	interface User {
		firstName?: string
		lastName?: string
		email?: string | null
		id?: string
		contactAddress?: {
			id?: string
		}
	}
}

declare module 'next-auth/jwt' {
	/** Returned by the `jwt` callback and `getToken`, when using JWT sessions */
	interface JWT {
		refreshTokenExpires?: number
		accessTokenExpires?: number
		refreshToken?: string
		token: string
		exp?: number
		iat?: number
		jti?: string
	}
}
