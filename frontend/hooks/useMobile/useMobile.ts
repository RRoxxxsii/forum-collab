import { useLayoutEffect, useState } from 'react'

interface useMobileResult {
	isMobile: boolean
}

export const useMobile = (): useMobileResult => {
	const [isMobile, setIsMobile] = useState(false)

	useLayoutEffect(() => {
		setIsMobile(window.innerWidth < 1000)
	}, [])

	return { isMobile }
}
