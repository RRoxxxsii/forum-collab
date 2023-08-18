import Cookies from 'js-cookie'
import { NextApiRequest } from 'next'

export async function GET(req: NextApiRequest): Promise<boolean> {
	const accessToken = req.cookies.access_token
	const refreshToken = req.cookies.refresh_token
	console.log('accessToken:', accessToken)
	console.log('refreshToken:', refreshToken)
	if (accessToken) {
		return true
	}

	if (!accessToken && !refreshToken) {
		return false
	}

	if (!accessToken && refreshToken) {
		const response = await fetch(
			'http://localhost:8000/api/v1/account/refresh/',
			{
				method: 'POST',
				body: JSON.stringify({ refreshToken }),
				headers: {
					'Content-Type': 'application/json',
				},
			}
		)
		const data = await response.json() // Await the JSON parsing

		const newAccessToken = data.access_token

		Cookies.set('access_token', newAccessToken, { expires: 86400 })

		return true
	}

	return false
}
