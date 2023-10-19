import { BASE_URL } from '@/shared/constants'
import { NextApiRequest } from 'next'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	try {
		const session = cookies().get('access_token')?.value

		if (!req.body) {
			return 
		}
		const { tags, title, content, uploaded_images } = await req.json()

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
		return NextResponse.json({ data }, { status: 200 })
	} catch (error: any | unknown) {
		return NextResponse.json({ message: error.message }, { status: 500 })
	}
}
