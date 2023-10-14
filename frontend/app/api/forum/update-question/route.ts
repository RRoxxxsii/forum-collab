import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const { user, title, content, id } = await req.json()

	if (!id) {
		return NextResponse.json({ error: 'Айди поста не было передано' })
	}
	const access_token = cookies().get('access_token')?.value

	const response = await fetch(`${BASE_URL}/forum/update-question/${id}/`, {
		method: 'PUT',
		body: JSON.stringify({ user: user, title: title, content: content }),
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${access_token ?? ''}`,
		},
	})
	const result = await response.json()

	if (response.ok) {
		return NextResponse.json({ ...result })
	} else {
		return NextResponse.json({ ...result }, { status: 500 })
	}
}
