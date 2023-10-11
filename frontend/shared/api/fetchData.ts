import { IQuestion, IUser } from '@/types/types'
import { Dispatch, SetStateAction } from 'react'

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
	} catch (error) {
		console.log(error)
	}
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
	} catch (error) {
		console.log(error)
	}
}
