import { BASE_URL } from '@/shared/constants'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	try {
		if (!req.body) {
			return null
		}
		const { email } = await req.json()

		const res = await fetch(`${BASE_URL}/account/password_reset/`, {
			method: 'POST',
			body: JSON.stringify({
				email: email,
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
		return NextResponse.json({ ...data }, { status: 200 })
	} catch (error: any | unknown) {
		return NextResponse.json(
			{ message: error?.message },
			{ status: error?.status }
		)
	}
}
