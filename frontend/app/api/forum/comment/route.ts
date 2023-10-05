import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const { comment, question_answer } = await req.json()

	const access_token = cookies().get('access_token')?.value
	console.log(access_token)

	if (!comment || !question_answer) {
		return NextResponse.json({ error: 'ID or Model was not provided' })
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
		return NextResponse.json({ message: result })
	} else {
		return NextResponse.json({ error: result }, { status: 500 })
	}
}
