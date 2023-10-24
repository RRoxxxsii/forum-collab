import type { NextRequest } from 'next/server'
import { NextResponse } from 'next/server'
import { BASE_URL } from './shared/constants'

export async function middleware(request: NextRequest) {
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
		return response
	} catch (error) {}
}
