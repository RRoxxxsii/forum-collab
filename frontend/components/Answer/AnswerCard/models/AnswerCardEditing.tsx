import { AddComment } from '@/components/Comment/AddComment'
import { IUser, IAnswer } from '@/types'
import { Box, Divider } from '@mui/material'
import React, { SetStateAction } from 'react'

export const AnswerCardEditing = ({
	isCommenting,
	answerData,
	answerHeight,
	setIsCommenting,
	userDetails,
}: {
	isCommenting: boolean
	answerHeight: number | undefined
	setIsCommenting: React.Dispatch<SetStateAction<boolean>>
	userDetails: IUser | null
	answerData: IAnswer
}) => {
	return (
		isCommenting && (
			<Box sx={{ display: 'flex', alignItems: 'center' }}>
				<Divider
					orientation='vertical'
					sx={{
						ml: 1.2,
						height: answerHeight ? answerHeight : 0,
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
