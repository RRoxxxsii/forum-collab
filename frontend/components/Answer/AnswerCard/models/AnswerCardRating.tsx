import { ChangeRating } from '@/shared/api/changeRating'
import { IUser, IAnswer, IChangeRating } from '@/types'
import {
	ArrowUpwardOutlined,
	ArrowUpward,
	ArrowDownwardOutlined,
	ArrowDownward,
} from '@mui/icons-material'
import { Checkbox } from '@mui/material'
import React, { useEffect, useState } from 'react'

export const AnswerCardRating = ({
	answerData,
	userDetails,
}: {
	userDetails: IUser | null
	answerData: IAnswer
}) => {
	const [clientRating, setClientRating] = useState(0)
	const [checked, setChecked] = useState<null | number>(null)

	const handleRating = ({ id, model, action, checked }: IChangeRating) => {
		ChangeRating({ id: id, model: model, action: action })
		if (checked) {
			setClientRating(
				(clientRating) => (clientRating = action === 'like' ? 1 : -1)
			)
			setChecked(action === 'like' ? 0 : 1)
		} else {
			setClientRating(
				(clientRating) => (clientRating += action === 'like' ? -1 : 1)
			)
			setChecked(null)
		}
	}

	useEffect(() => {
		if (answerData.rating.is_liked) {
			setChecked(0)
		}
		if (answerData.rating.is_disliked) {
			setChecked(1)
		}
	}, [answerData.rating.is_disliked, answerData.rating.is_liked])

	return (
		<>
			<Checkbox
				disabled={answerData?.user?.id === userDetails?.id}
				checked={checked === 0}
				icon={<ArrowUpwardOutlined />}
				checkedIcon={<ArrowUpward />}
				onChange={(e) =>
					handleRating({
						id: answerData.id,
						model: 'answer',
						action: 'like',
						checked: e.target.checked,
					})
				}
			/>
			{answerData?.rating?.like_amount -
				answerData?.rating?.dislike_amount +
				clientRating || 0}
			<Checkbox
				disabled={answerData?.user?.id === userDetails?.id}
				checked={checked === 1}
				icon={<ArrowDownwardOutlined />}
				checkedIcon={<ArrowDownward />}
				onChange={(e) =>
					handleRating({
						id: answerData.id,
						model: 'answer',
						action: 'dislike',
						checked: e.target.checked,
					})
				}
			/>
		</>
	)
}
