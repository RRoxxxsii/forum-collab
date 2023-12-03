'use client'
import { AddComment } from '@/components/Comment/AddComment'
import { useElementSize } from '@/lib/hooks/useElementSize'
import { IUser, IAnswer } from '@/types'
import { Box, Divider } from '@mui/material'
import React, { SetStateAction } from 'react'

export const AnswerCardEditing = ({
	isCommenting,
	answerData,
	setIsCommenting,
	userDetails,
}: {
	isCommenting: boolean
	setIsCommenting: React.Dispatch<SetStateAction<boolean>>
	userDetails: IUser | null
	answerData: IAnswer
}) => {
	const [commentAddBox, { width, height }] = useElementSize()

	return (
		isCommenting && (
			<Box sx={{ display: 'flex', alignItems: 'center' }}>
				<Divider
					orientation='vertical'
					sx={{
						ml: 1.2,
						height: height ? height : 0,
					}}
				/>
				<Box sx={{ flex: '0 1 100%' }}>
					<AddComment
						isCommenting={isCommenting}
						setIsCommenting={setIsCommenting}
						profileData={userDetails}
						answerData={answerData}
					/>
				</Box>
			</Box>
		)
	)
}
