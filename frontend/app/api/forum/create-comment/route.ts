import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const { comment, question_answer } = await req.json()

	const access_token = cookies().get('access_token')?.value

	if (!comment || !question_answer) {
		return NextResponse.json(
			{ error: 'ID или Модель неизвестны' },
			{ status: 422 }
		)
	}

	if (question_answer.length < 1) {
		return NextResponse.json(
			{ error: 'Коммент слишком короткое' },
			{ status: 422 }
		)
	}

	const response = await fetch(`${BASE_URL}/forum/create-comment/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${access_token ?? ''}`,
		},
		body: JSON.stringify({
			comment: comment,
			question_answer: question_answer,
		}),
	})
	const result = await response.json()

	if (response.ok) {
		return NextResponse.json({ ...result }, { status: response.status })
	} else {
		return NextResponse.json({ error: result }, { status: response.status })
	}
}
