import { BASE_URL } from '@/shared/constants'
import { Model } from '@/types/types'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	const { id, model }: { id: number; model: Model } = await req.json()

	if (!id || !model) {
		return NextResponse.json(
			{ error: 'ID или Модель неизвестны' },
			{ status: 422 }
		)
	}
	const access_token = cookies().get('access_token')?.value

	try {
		const response = await fetch(`${BASE_URL}/forum/update-${model}/${id}/`, {
			method: 'DELETE',
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
	} catch (error) {
		return NextResponse.json({ error: error })
	}
}
