import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	if (!req.body) {
		return null
	}
	const { email } = await req.json()

	const res = await fetch(
		'http://localhost:8000/api/v1/account/restore-account/',
		{
			method: 'POST',
			body: JSON.stringify({
				email: email,
			}),
			headers: { 'Content-Type': 'application/json' },
		}
	)

	const data = await res.json()

	if (!res.ok) {
		return NextResponse.json(
			{
				...data,
			},
			{ status: 401 }
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
}
