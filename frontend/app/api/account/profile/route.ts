import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const access_token = cookies().get('access_token')?.value

	const { userId } = await req.json()

	const response = await fetch(`${BASE_URL}/account/users/${userId}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `${access_token ? `Bearer ${access_token}` : ''}`,
		},
	})
	const result = await response.json()

	if (response.ok) {
		return NextResponse.json(result)
	} else {
		return NextResponse.json({ error: result }, { status: response.status })
	}
}
