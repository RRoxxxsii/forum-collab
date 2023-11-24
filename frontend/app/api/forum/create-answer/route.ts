import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const {
		question_id,
		answer_content,
	}: { question_id: number; answer_content: string } = await req.json()

	const access_token = cookies().get('access_token')?.value

	if (!question_id || !answer_content) {
		return NextResponse.json(
			{ error: 'ID или ответ неизвестен' },
			{ status: 422 }
		)
	}

	if (answer_content.length < 10) {
		return NextResponse.json(
			{ error: 'Ответ слишком короткий' },
			{ status: 400 }
		)
	}

	const response = await fetch(`${BASE_URL}/forum/answer-question/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `${access_token ? `Bearer ${access_token}` : ''}`,
		},
		body: JSON.stringify({
			question: question_id,
			answer: answer_content,
		}),
	})
	const result = await response.json()

	if (response.ok) {
		return NextResponse.json({ ...result }, { status: response.status })
	} else {
		return NextResponse.json({ error: result }, { status: response.status })
	}
}
