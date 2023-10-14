import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const { question_answer_id } = await req.json()

	const access_token = cookies().get('access_token')?.value

	if (!question_answer_id) {
		return NextResponse.json({ error: 'Айди вопроса не было передано' })
	}
	const response = await fetch(
		`${BASE_URL}/forum/mark-answer-solving/${question_answer_id}/`,
		{
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${access_token ?? ''}`,
			},
		}
	)
	const result = await response.json()
	console.log(result)

	if (response.ok) {
		return NextResponse.json({ ...result })
	} else {
		return NextResponse.json({ error: result.detail }, { status: 500 })
	}
}
