import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const { question_id, answer_content } = await req.json()

	const access_token = cookies().get('access_token')?.value

	if (!question_id || !answer_content) {
		return NextResponse.json({ error: 'Id или сам ответ не был предоставлен' })
	}
	const response = await fetch(`${BASE_URL}/forum/answer-question/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${access_token ?? ''}`,
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
		return NextResponse.json({ ...result }, { status: response.status })
	}
}
