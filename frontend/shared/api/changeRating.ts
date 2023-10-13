import { IAnswer, IQuestion } from '@/types/types'
import { Dispatch, SetStateAction } from 'react'
//TODO: MAKE THIS UPDATE ON CLIENT SIDE
export async function Dislike({
	id,
	model,
} // setNewState
: {
	id: number
	model: 'question' | 'answer'
	// setNewState: Dispatch<SetStateAction<IQuestion | IAnswer>>
}) {
	try {
		const response = await fetch(`/api/forum/dislike`, {
			method: 'POST',
			body: JSON.stringify({ id: id, model: model }),
			headers: {
				'Content-Type': 'application/json',
			},
		})
		const data = await response.json()

		if (!response.ok) {
			throw new Error(data)
		}
		// setNewState(data)
		return data
	} catch (error) {
		console.log(error)
	}
}

export async function Like({
	id,
	model,
} // setNewState
: {
	id: number
	model: 'question' | 'answer'
	// setNewState: Dispatch<SetStateAction<IQuestion | IAnswer>>
}) {
	try {
		const response = await fetch(`/api/forum/like`, {
			method: 'POST',
			body: JSON.stringify({ id: id, model: model }),
			headers: {
				'Content-Type': 'application/json',
			},
		})

		const data = await response.json()

		if (!response.ok) {
			throw new Error(data)
		}
		// setNewState(data)
		return data
	} catch (error) {
		console.log(error)
	}
}
