import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const { question, answer } = await req.json()

	if (!question || !answer) {
		return NextResponse.json(
			{ error: 'ID вопроса или ответа неизвестны' },
			{ status: 422 }
		)
	}

	if (answer.length < 10) {
		return NextResponse.json(
			{ error: 'Ответ слишком короткий' },
			{ status: 400 }
		)
	}

	const access_token = cookies().get('access_token')?.value

	const response = await fetch(`${BASE_URL}/forum/update-answer/${question}/`, {
		method: 'PUT',
		body: JSON.stringify({
			question: question,
			answer: answer,
		}),
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${access_token ?? ''}`,
		},
	})
	const result = await response.json()

	if (response.ok) {
		return NextResponse.json({ ...result }, { status: response.status })
	} else {
		return NextResponse.json({ error: result }, { status: response.status })
	}
}
