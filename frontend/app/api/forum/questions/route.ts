import { BASE_URL } from '@/shared/constants'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const { page_id } = await req.json()

	if (!page_id) {
		return NextResponse.json({ error: 'Айди поста не было передано' })
	}

	const response = await fetch(`${BASE_URL}/forum/questions/${page_id}/`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
		},
	})
	const result = await response.json()

	if (response.ok) {
		return NextResponse.json({ ...result })
	} else {
		return NextResponse.json({ error: result }, { status: 500 })
	}
}
