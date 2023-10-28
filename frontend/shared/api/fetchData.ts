import { CategoryType, IQuestion, IUser } from '@/types'
import { Dispatch, SetStateAction } from 'react'
import { BASE_URL } from '../constants'

export async function fetchQuestions({ category }: { category: CategoryType }) {
	try {
		const response = await fetch(
			`${BASE_URL}/forum/questions/?limit=10&sort=${category}`,
			{
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
				},
			}
		)

		const result = await response.json()

		if (!response.ok || !Array.isArray(result)) {
			throw new Error('Failed to fetch questions')
		}

		return result
	} catch (error) {
		return error
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
