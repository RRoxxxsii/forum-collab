import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
	// Assume a "Cookie:nextjs=fast" header to be present on the incoming request
	// Getting cookies from the request using the `RequestCookies` API
	let cookie = request.cookies.get('access_token')
	console.log(cookie) // => { name: 'nextjs', value: 'fast', Path: '/' }

	// Setting cookies on the response using the `ResponseCookies` API
	const response = NextResponse.next()

	cookie = response.cookies.get('vercel')
	console.log(cookie) // => { name: 'vercel', value: 'fast', Path: '/' }
	// The outgoing response will have a `Set-Cookie:vercel=fast;path=/test` header.

	return response
}
