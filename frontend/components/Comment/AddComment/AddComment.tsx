'use client'
import { useElementSize } from '@/lib/hooks/useElementSize'
import { useOnClickOutside } from '@/lib/hooks/useOnClickOutside'
import { IAnswer, IComment, IUser } from '@/types'
import { TextareaAutosize } from '@mui/base/TextareaAutosize'
import { Box, Button, Divider, Typography } from '@mui/material'
import React, { Dispatch, SetStateAction, useEffect, useRef } from 'react'

export const AddComment = ({
	answerData,
	parentComment = null,
	profileData,
	isCommenting,
	setIsCommenting,
}: {
	isCommenting: boolean
	parentComment?: null | IComment
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
					parent: parentComment?.id,
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
	const commentInputRef = useRef<HTMLTextAreaElement | null>(null)

	const handleClickOutside = (event: MouseEvent) => {
		setIsCommenting(false)
	}
	useOnClickOutside(commentBoxRef, handleClickOutside)
	const [commentBoxContentRef, { width, height }] = useElementSize()
	useEffect(() => {
		if (parentComment) {
			setCommentContent(
				`@${
					parentComment?.user?.user_name
						? parentComment?.user?.user_name
						: 'Гость'
				}, `
			)
		}
	}, [parentComment])

	useEffect(() => {
		if (isCommenting) {
			commentInputRef.current?.focus()
		}
	}, [isCommenting])

	return (
		<Box
			ref={commentBoxContentRef}
			sx={{
				display: 'flex',
				alignItems: 'center',
				justifyContent: 'flex-start',
				flex: 1,
			}}>
			<Box
				ref={commentBoxRef}
				sx={{
					flex: 1,
					mb: 2,
					pl: 4,
					display: 'flex',
					flexDirection: 'column',
					maxWidth: 600,
				}}>
				<Typography variant='caption' color={'GrayText'}>
					Вы отвечаете пользователю{' '}
					{'@' +
						((parentComment
							? parentComment?.user?.user_name
							: answerData?.user?.user_name) ?? 'Гость')}
				</Typography>
				<TextareaAutosize
					ref={commentInputRef}
					minRows={2}
					onChange={(e) => setCommentContent(e.target.value)}
					value={commentContent}
					className='textarea w-full'
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
		</Box>
	)
}
