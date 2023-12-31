import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const { page_id } = await req.json()

	const access_token = cookies().get('access_token')?.value

	if (!page_id) {
		return NextResponse.json(
			{ error: 'ID вопроса неизвестны' },
			{ status: 422 }
		)
	}

	const response = await fetch(`${BASE_URL}/forum/questions/${page_id}/`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${access_token ?? ''}`,
		},
	})
	const result = await response.json()

	if (response.ok) {
		return NextResponse.json({ ...result })
	} else {
		return NextResponse.json({ error: result }, { status: response.status })
	}
}
