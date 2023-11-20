import { BASE_URL } from '@/shared/constants'
import { revalidatePath } from 'next/cache'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const {
		id,
		model,
		action,
	}: { id: number; model: 'question' | 'answer'; action: 'like' | 'dislike' } =
		await req.json()

	const access_token = cookies().get('access_token')?.value

	if (!id || !model) {
		return NextResponse.json(
			{ error: 'ID или Модель неизвестны' },
			{ status: 422 }
		)
	}
	const response = await fetch(
		`${BASE_URL}/forum/likes/${id}/${action}/?model=${model}`,
		{
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${access_token ?? ''}`,
			},
		}
	)
	const result = await response.json()

	if (response.ok) {
		const path = req.nextUrl.searchParams.get('path')

		if (path) {
			revalidatePath(path)
			return Response.json({ revalidated: true, now: Date.now() })
		}
		return NextResponse.json({ result }, { status: response.status })
	} else {
		return NextResponse.json({ error: result }, { status: response.status })
	}
}
