import { BASE_URL } from '@/shared/constants'
import { IUser } from '@/types'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET() {
	const access_token = cookies().get('access_token')?.value

	const response = await fetch(`${BASE_URL}/account/me/`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${access_token ?? ''}`,
		},
	})
	const result: IUser = await response.json()

	if (response.ok) {
		return NextResponse.json({ ...result })
	} else {
		return NextResponse.json({ error: result }, { status: response.status })
	}
}
