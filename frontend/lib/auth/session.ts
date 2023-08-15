import { getServerSession } from 'next-auth/next'
import { authOptions } from '.'

export default async function Page() {
	const session = await getServerSession(authOptions)

	return session?.user
}
