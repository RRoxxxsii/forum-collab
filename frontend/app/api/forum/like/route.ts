import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const { id, model } = await req.json()

	const access_token = cookies().get('access_token')?.value

	if (!id || !model) {
		return NextResponse.json({ error: 'ID or Model was not provided' })
	}
	const response = await fetch(
		`${BASE_URL}/forum/likes/${id}/like/?model=${model}`,
		{
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${access_token ?? ''}`,
			},
		}
	)
	const result = await response.json()

	if (response.ok) {
		return NextResponse.json({ message: result })
	} else {
		return NextResponse.json({ error: result }, { status: 500 })
	}
}
