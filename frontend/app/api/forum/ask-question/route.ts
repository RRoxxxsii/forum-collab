import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	try {
		const session = cookies().get('access_token')?.value

		const { tags, title, content, uploaded_images } = await req.json()

		if (content.length < 10) {
			return NextResponse.json(
				{ error: 'Описание вопроса слишком короткое' },
				{ status: 400 }
			)
		}

		const res = await fetch(`${BASE_URL}/forum/ask-question/`, {
			method: 'POST',
			body: JSON.stringify({
				tags,
				title,
				content,
				uploaded_images,
			}),
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${session}`,
			},
		})

		const data = await res.json()

		if (!res.ok) {
			let errorMessage = ''
			if (data?.code) {
				errorMessage +=
					'Ваша текущая сессия истекла, попробуйте перезагрузить страницу '
			}
			if (data?.tags) {
				errorMessage += 'Теги: '
				data.tags.forEach((error: string) => {
					errorMessage += error + ' '
				})
			}
			if (data?.title) {
				errorMessage += '\nЗаголовок: '
				data.tags.forEach((error: string) => {
					errorMessage += error + ' '
				})
			}
			return NextResponse.json(
				{
					error: errorMessage,
				},
				{ status: res.status }
			)
		}
		return NextResponse.json({ ...data }, { status: res.status })
	} catch (error: any | unknown) {
		return NextResponse.json({ error: error.message }, { status: 500 })
	}
}

export async function GET(req: NextRequest) {
	try {
		const session = cookies().get('access_token')?.value

		const { searchParams } = new URL(req.url ?? '')
		const q = searchParams.get('q')

		const res = await fetch(`${BASE_URL}/forum/ask-question/?q=${q}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${session}`,
			},
		})

		const data = await res.json()
		if (!res.ok) {
			return NextResponse.json(
				{
					...data,
				},
				{ status: res.status }
			)
		}
		return NextResponse.json({ data }, { status: res.status })
	} catch (error: any | unknown) {
		return NextResponse.json({ message: error.message }, { status: 500 })
	}
}
