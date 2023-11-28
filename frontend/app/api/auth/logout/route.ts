import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function GET(req: NextRequest) {
	try {
		cookies().delete({
			name: 'access_token',
			httpOnly: true,
			maxAge: 60 * 60,
		})
		cookies().delete({
			name: 'refresh_token',
			httpOnly: true,
			maxAge: 60 * 60 * 60 * 24,
		})

		return NextResponse.json({ message: 'Выход' }, { status: 200 })
	} catch (error) {
		const errorMessage =
			error instanceof Error
				? error.message
				: 'An error occured. Please check username and password.'
		return NextResponse.json(
			{ error: errorMessage, ok: false },
			{ status: 503 }
		)
	}
}
