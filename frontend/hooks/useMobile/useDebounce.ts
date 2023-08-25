import { useCallback, useRef } from 'react'

interface DebounceType {
	callback: (...args: any[]) => void
	delay: number
}

export function useDebounce(callback: (...args: any[]) => void, delay: number) {
	const timer = useRef<ReturnType<typeof setTimeout> | null>(null)

	const debouncedCallback = useCallback(
		(...args: Parameters<typeof callback>) => {
			if (timer.current) {
				clearTimeout(timer.current)
			}

			timer.current = setTimeout(() => {
				callback(...args)
			}, delay)
		},
		[callback, delay]
	)

	return debouncedCallback
}
