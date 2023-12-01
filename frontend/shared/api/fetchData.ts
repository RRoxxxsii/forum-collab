import { CategoryType, INotifications, IUser } from '@/types'
import { Dispatch, SetStateAction } from 'react'
import { BASE_URL } from '../constants'
import { IQuestion } from './../../types/index'

interface FetchQuestionProps {
	category: CategoryType
	page: number
}

export async function fetchQuestions<T>({
	category,
	page,
}: FetchQuestionProps): Promise<T[] | string> {
	try {
		const response = await fetch(
			`${BASE_URL}/forum/questions/?&sort=${category}&page=${page ?? 0}`,
			{
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
				},
			}
		)

		const result: T[] = await response.json()

		if (!response.ok || !Array.isArray(result)) {
			throw new Error('Failed to fetch questions')
		}

		return result
	} catch (error) {
		if (typeof error === 'string') {
			return error
		}
		if (error instanceof Error) {
			return error.message
		}
		return ''
	}
}

export async function fetchQuestion({
	setQuestionData,
	id,
}: {
	setQuestionData: Dispatch<SetStateAction<IQuestion | null>>
	id: string | number | null
}) {
	try {
		if (!setQuestionData || !id) return null

		const response = await fetch(`/api/forum/questions`, {
			method: 'POST',
			body: JSON.stringify({ page_id: id }),
			headers: {
				'Content-Type': 'application/json',
			},
		})

		const result: IQuestion | string = await response.json()
		if (!response.ok) {
			if (typeof result !== 'string') return null
			throw new Error(result)
		}

		if (typeof result === 'object' && 'id' in result) {
			setQuestionData(result)
		}
	} catch (error) {}
}

export async function fetchMe({
	setProfileData,
}: {
	setProfileData: Dispatch<SetStateAction<IUser | null>>
}) {
	try {
		if (setProfileData === null) return null

		const response = await fetch(`/api/account/me/`)

		const result = await response.json()
		if (!response.ok) {
			throw new Error(result)
		}

		setProfileData(result)
	} catch (error) {}
}

export async function fetchNotifications({
	setNotifications,
}: {
	setNotifications: Dispatch<SetStateAction<INotifications[]>>
}) {
	try {
		if (setNotifications === null) return null

		const response = await fetch(`/api/account/notifications/`)

		const result = await response.json()

		if (!response.ok) {
			throw new Error(result)
		}

		setNotifications(result)
	} catch (error) {}
}
