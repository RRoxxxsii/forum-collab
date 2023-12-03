import { BASE_URL } from '@/shared/constants'
import { NextRequest, NextResponse } from 'next/server'

export async function GET(req: NextRequest) {
	const hasRefreshToken = req.cookies.has('refresh_token')
	const refreshTokenCookie = req.cookies.get('refresh_token')

	if (!hasRefreshToken) {
		return NextResponse.json({ message: 'Вы не авторизованы' }, { status: 403 })
	}

	const response = NextResponse.next()
	const isAuth = await fetch(`${BASE_URL}/account/refresh/`, {
		method: 'POST',
		next: { revalidate: 3600 },
		body: JSON.stringify({ refresh: refreshTokenCookie }),
		headers: {
			'Content-Type': 'application/json',
		},
	})

	const data = await isAuth.json()
	const newAccessToken = data.access

	response.cookies.set({ name: 'access_token', value: newAccessToken })
	response.headers.set('access_token', newAccessToken)
	return response
}
