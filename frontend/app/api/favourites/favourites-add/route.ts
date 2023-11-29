import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const { question } = await req.json()

	const access_token = cookies().get('access_token')?.value

	if (!question) {
		return NextResponse.json(
			{ error: 'ID или Модель неизвестны' },
			{ status: 422 }
		)
	}

	const response = await fetch(`${BASE_URL}/favourites/favourites-add/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `${access_token ? `Bearer ${access_token}` : ''}`,
		},
		body: JSON.stringify({
			question: question,
		}),
	})
	const result = await response.json()

	if (response.ok) {
		return NextResponse.json({ ...result }, { status: response.status })
	} else {
		return NextResponse.json({ ...result }, { status: response.status })
	}
}
