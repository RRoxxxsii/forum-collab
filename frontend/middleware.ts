import type { NextRequest } from 'next/server'
import { NextResponse } from 'next/server'

export async function middleware(request: NextRequest) {
	const accessTokenCookie = request.cookies.get('access_token')
	const refreshTokenCookie = request.cookies.get('refresh_token')
	const response = NextResponse.next()
	//if user's access token is valid then get a response
	if (accessTokenCookie) {
		return response
	}
	//if user access token AND refresh token is not valid return null
	if (!accessTokenCookie && !refreshTokenCookie) {
		return null
	}
	//if user has an acess token but the refresh token is already expired
	if (!refreshTokenCookie) {
		response.cookies.delete('access_token')
		return response
	}
	//the situation when user doesn't have an access token, but has a refresh one.
	//create new access token
	try {
		const isAuth = await fetch(
			'http://localhost:8000/api/v1/account/refresh/',
			{
				method: 'POST',
				body: JSON.stringify({ refresh: refreshTokenCookie?.value }),
				headers: {
					'Content-Type': 'application/json',
				},
			}
		)
		const data = await isAuth.json()

		const newAccessToken = data.access

		response.cookies.set({ name: 'access_token', value: newAccessToken })
		console.log('token refreshed!')
		return response
	} catch (error) {
		console.log(error)
	}
}
