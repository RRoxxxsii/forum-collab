import { BASE_URL } from '@/shared/constants'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
	try {
		if (!req.body) {
			return
		}
		const { email, user_name, password } = await req.json()

		const response = await fetch(`${BASE_URL}/account/create-account/`, {
			method: 'POST',
			body: JSON.stringify({
				email: email,
				password: password,
				user_name: user_name,
			}),
			headers: { 'Content-Type': 'application/json' },
		})

		const data = await response.json()

		if (!response.ok) {
			let errorMessage = ''
			if (data?.email) {
				data?.email.forEach((error: string) => {
					errorMessage += error + ' '
				})
			}
			if (data?.user_name) {
				data?.user_name.forEach((error: string) => {
					errorMessage += error + ' '
				})
			}
			if (data?.password) {
				data?.password.forEach((error: string) => {
					errorMessage += error + ' '
				})
			}
			return NextResponse.json(
				{
					message: errorMessage,
				},
				{ status: response.status }
			)
		}

		return NextResponse.json(
			{ message: 'Вы успешно зарегистрировались!' },
			{ status: response.status }
		)
	} catch (error) {
		return
	}
}
