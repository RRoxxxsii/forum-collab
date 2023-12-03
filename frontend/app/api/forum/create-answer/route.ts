import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const {
		question_id,
		answer_content,
		answerImages,
	}: { question_id: number; answer_content: string; answerImages?: File[] } =
		await req.json()

	let formField = new FormData()

	formField.append('question', question_id.toString())
	formField.append('answer', answer_content)
	answerImages?.forEach((image) => {
		formField.append('uploaded_images', image)
	})

	console.log(formField)

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
			'Content-Type':
				'multipart/form-data; boundary=WebKitFormBoundary8X8G66ilD7YqGFuL',
			Authorization: `${access_token ? `Bearer ${access_token}` : ''}`,
		},
		body: formField,
	})
	const result = await response.json()

	if (response.ok) {
		return NextResponse.json({ ...result }, { status: response.status })
	} else {
		return NextResponse.json({ error: result }, { status: response.status })
	}
}
