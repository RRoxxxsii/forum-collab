import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET() {
	const refreshTokenCookie = cookies().get('refresh_token')?.value

	if (!refreshTokenCookie) {
		return NextResponse.json({ message: 'Вы не авторизованы' }, { status: 403 })
	}

	try {
		const isAuth = await fetch(`${BASE_URL}/account/refresh/`, {
			method: 'POST',
			body: JSON.stringify({ refresh: refreshTokenCookie }),
			headers: {
				'Content-Type': 'application/json',
			},
		})
		const response = NextResponse.next()

		const data = await isAuth.json()
		const newAccessToken = data.access

		response.cookies.delete('access_token')

		response.cookies.set({ name: 'access_token', value: newAccessToken })

		return response
	} catch (error) {}
}
