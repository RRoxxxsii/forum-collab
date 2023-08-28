import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	try {
		if (!req.body) {
			return null
		}
		const { email, password } = await req.json()

		const res = await fetch(`${BASE_URL}/account/token/`, {
			method: 'POST',
			body: JSON.stringify({
				email: email,
				password: password,
			}),
			headers: { 'Content-Type': 'application/json' },
		})

		const data = await res.json()

		if (!res.ok) {
			return NextResponse.json(
				{
					...data,
				},
				{ status: res.status }
			)
		}

		cookies().set({
			name: 'access_token',
			value: data.access,
			httpOnly: true,
			maxAge: 60 * 60,
		})
		cookies().set({
			name: 'refresh_token',
			value: data.refresh,
			httpOnly: true,
			maxAge: 60 * 60 * 60 * 24,
		})

		return NextResponse.json(
			{ message: 'Вы успешно авторизовались!' },
			{ status: 200 }
		)
	} catch (error) {
		return null
	}
}
