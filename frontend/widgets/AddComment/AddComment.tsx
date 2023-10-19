'use client'
import { IAnswer, IComment, IUser } from '@/types/types'
import { TextareaAutosize } from '@mui/base/TextareaAutosize'
import { Box, Button, Typography } from '@mui/material'
import React, {
	Dispatch,
	MouseEventHandler,
	SetStateAction,
	useEffect,
	useRef,
} from 'react'

export const AddComment = ({
	answerData,
	profileData,
	isCommenting,
	setIsCommenting,
}: {
	isCommenting: boolean
	setIsCommenting: Dispatch<SetStateAction<boolean>>
	answerData: IAnswer
	profileData: IUser | null
}) => {
	const [commentContent, setCommentContent] = React.useState('')

	const handleComment = async () => {
		if (commentContent.length > 0 && commentContent.length < 320) {
			const response = await fetch('/api/forum/create-comment', {
				method: 'POST',
				body: JSON.stringify({
					user: profileData,
					comment: commentContent,
					question_answer: answerData.id,
				}),
			})

			if (!response.ok) {
				return
			}

			const data: IComment = await response.json()
			answerData.comments.push({
				comment: data?.comment,
				question_answer: data?.question_answer,
				creation_date: data?.creation_date,
				id: data?.id,
				user: data?.user,
			})

			setCommentContent('')
			setIsCommenting(false)
		}
	}
	const commentBoxRef = useRef<HTMLDivElement | null>(null)
	const handleClickOutside = (event: MouseEvent) => {
		if (
			commentBoxRef.current &&
			!commentBoxRef.current.contains(event.target as Node)
		) {
			setIsCommenting(false)
		}
	}

	useEffect(() => {
		if (isCommenting) {
			document.addEventListener('click', handleClickOutside)
		} else {
			document.removeEventListener('click', handleClickOutside)
		}

		return () => {
			document.removeEventListener('click', handleClickOutside)
		}
	}, [isCommenting])

	return (
		<Box
			ref={commentBoxRef}
			sx={{
				mb: 2,
				pl: 4,
				display: 'flex',
				flexDirection: 'column',
				maxWidth: 600,
			}}>
			<Typography variant='caption' color={'GrayText'}>
				Вы отвечаете пользователю{' '}
				{'@' + (answerData?.user?.user_name ?? 'Гость')}
			</Typography>

			<TextareaAutosize
				minRows={2}
				onChange={(e) => setCommentContent(e.target.value)}
				className='textarea'
				maxLength={320}
			/>
			<Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
				<Button
					onClick={handleComment}
					variant='outlined'
					sx={{ mt: 1, maxWidth: 220 }}>
					Оставить комментарий
				</Button>
				<Typography
					sx={{ userSelect: 'none' }}
					color={'ButtonHighlight'}
					variant='caption'>
					{commentContent.length}/320
				</Typography>
			</Box>
		</Box>
	)
}
