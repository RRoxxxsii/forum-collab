import { IChangeRating, IModelType } from '@/types'

export async function ChangeRating({ id, model, action }: IChangeRating) {
	try {
		const response = await fetch(`/api/forum/change-rating`, {
			method: 'POST',
			body: JSON.stringify({ id: id, model: model, action: action }),
			headers: {
				'Content-Type': 'application/json',
			},
		})
		const data = await response.json()

		if (!response.ok) {
			throw new Error(data)
		}
		return data
	} catch (error) {}
}
