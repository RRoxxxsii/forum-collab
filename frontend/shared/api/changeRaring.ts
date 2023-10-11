export async function dislikeQuestion({ id }: { id: number }) {
	try {
		const response = await fetch(`/api/forum/dislike`, {
			method: 'POST',
			body: JSON.stringify({ id: id, model: 'question' }),
			headers: {
				'Content-Type': 'application/json',
			},
		})
		const data = await response.json()

		if (!response.ok) {
			throw new Error(data)
		}

		return data
	} catch (error) {
		console.log(error)
	}
}

export async function likeQuestion({ id }: { id: number }) {
	try {
		const response = await fetch(`/api/forum/like`, {
			method: 'POST',
			body: JSON.stringify({ id: id, model: 'question' }),
			headers: {
				'Content-Type': 'application/json',
			},
		})

		const data = await response.json()

		if (!response.ok) {
			throw new Error(data)
		}

		return data
	} catch (error) {
		console.log(error)
	}
}
