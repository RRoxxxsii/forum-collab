import type { NextRequest } from 'next/server'
import { NextResponse } from 'next/server'
import { BASE_URL } from './shared/constants'

export const config = {
	matcher: ['/profile/:path*', '/settings/:path*'],
}

export async function middleware(request: NextRequest) {
	const hasRefreshToken = request.cookies.has('refresh_token')

	if (request.nextUrl.pathname.startsWith('/profile') && !hasRefreshToken) {
		return NextResponse.rewrite(new URL('/', request.url))
	}

	if (request.nextUrl.pathname.startsWith('/settings')) {
		return NextResponse.rewrite(new URL('/', request.url))
	}

	if (!hasRefreshToken) {
		return
	}
	console.log('click')

	const refreshTokenCookie = request.cookies.get('refresh_token')
	const response = NextResponse.next()
	try {
		const isAuth = await fetch(`${BASE_URL}/account/refresh/`, {
			method: 'POST',
			body: JSON.stringify({ refresh: refreshTokenCookie?.value }),
			headers: {
				'Content-Type': 'application/json',
			},
		})
		const data = await isAuth.json()

		const newAccessToken = data.access

		response.cookies.set({ name: 'access_token', value: newAccessToken })
		response.headers.set('access_token', newAccessToken)
		return response
	} catch (error) {}
}
