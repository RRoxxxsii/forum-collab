import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	try {
		const session = cookies().get('access_token')?.value

		if (!req.body) {
			return null
		}
		const { tags, title, content, uploaded_images } = await req.json()

		// const token = await fetch('http://localhost:3000/api/auth/refresh', {
		// 	method: 'GET',
		// })

		const res = await fetch(`${BASE_URL}/forum/ask-question/`, {
			body: JSON.stringify({
				tags,
				title,
				content,
				uploaded_images,
			}),
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${session}`,
			},
		})

		const data = await res.json()

		console.log(data)

		if (!res.ok) {
			return NextResponse.json(
				{
					...data,
				},
				{ status: res.status }
			)
		}
		return NextResponse.json({ ...data }, { status: 200 })
	} catch (error: any | unknown) {
		return NextResponse.json({ message: error.message }, { status: 500 })
	}
}
