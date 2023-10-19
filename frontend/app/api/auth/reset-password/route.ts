import { BASE_URL } from '@/shared/constants'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	try {
		if (!req.body) {
			return
		}
		const { email } = await req.json()

		const response = await fetch(`${BASE_URL}/account/password_reset/`, {
			method: 'POST',
			body: JSON.stringify({
				email: email,
			}),
			headers: { 'Content-Type': 'application/json' },
		})

		const data = await response.json()

		if (!response.ok) {
			return NextResponse.json(
				{
					...data,
				},
				{ status: response.status }
			)
		}
		return NextResponse.json({ ...data }, { status: response.status })
	} catch (error: any | unknown) {
		return NextResponse.json(
			{ message: error?.message },
			{ status: error?.status }
		)
	}
}
