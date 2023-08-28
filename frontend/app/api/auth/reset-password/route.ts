import { BASE_URL } from '@/shared/constants'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	try {
		if (!req.body) {
			return null
		}
		const { email } = await req.json()

		const res = await fetch(`${BASE_URL}/account/restore-account/`, {
			method: 'POST',
			body: JSON.stringify({
				email: email,
			}),
			headers: { 'Content-Type': 'application/json' },
		})
		console.log(res)
		const data = await res.json()

		if (!res.ok) {
			return NextResponse.json(
				{
					message: data,
				},
				{ status: res.status }
			)
		}
		return NextResponse.json({ message: res.json() }, { status: 200 })
	} catch (error) {
		console.log(error)
	}
}
