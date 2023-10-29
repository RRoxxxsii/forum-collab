import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { IAnswer, IComment, IModelType } from '@/types'
import { AddComment } from '@/widgets/AddComment'
import { Comment, Delete, Edit, MoreHoriz, Report } from '@mui/icons-material'
import {
	Avatar,
	Box,
	Button,
	Checkbox,
	Divider,
	FormControlLabel,
	IconButton,
	Menu,
	MenuItem,
	TextareaAutosize,
	Typography,
} from '@mui/material'
import { green } from '@mui/material/colors'
import dayjs from 'dayjs'
import ru from 'dayjs/locale/ru'
import relativeTime from 'dayjs/plugin/relativeTime'
import React, { useContext, useEffect, useRef, useState } from 'react'

interface CommentCardProps {
	comment: IComment
	answerData: IAnswer
	handleDelete: ({ id, model }: { id: number; model: IModelType }) => void
}

export function CommentCard({
	comment,
	answerData,
	handleDelete,
}: CommentCardProps) {
	const { userDetails } = useContext(UserDetailsContext)

	const [moreButtonEl, setMoreButtonEl] = useState<HTMLElement | null>(null)

	const moreDropdownOpen = Boolean(moreButtonEl)
	const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
		setMoreButtonEl(event.currentTarget)
	}
	const handleClose = () => {
		setMoreButtonEl(null)
	}
	const [isCommenting, setIsCommenting] = useState<boolean>(false)

	const [isEditing, setIsEditing] = useState(false)

	const handleEditing = () => {
		setIsEditing(!isEditing)
	}
	const submitEditing = () => {
		setIsEditing(!isEditing)
	}
	const editingBoxRef = useRef<HTMLDivElement | null>(null)
	const handleClickOutside = (event: MouseEvent) => {
		if (
			editingBoxRef.current &&
			!editingBoxRef.current.contains(event.target as Node)
		) {
			setIsEditing(false)
		}
	}

	const [editingCommentContent, setEditingCommentContent] = useState('')

	useEffect(() => {
		if (isEditing) {
			document.addEventListener('click', handleClickOutside)
		} else {
			document.removeEventListener('click', handleClickOutside)
		}

		return () => {
			document.removeEventListener('click', handleClickOutside)
		}
	}, [isEditing])

	const commentRef = useRef<null | HTMLElement>(null)

	const [commentHeightOffset, setCommentHeightOffset] = useState<
		number | undefined
	>(0)
	const [commentHeightClient, setCommentHeightClient] = useState<
		number | undefined
	>(0)
	useEffect(() => {
		setCommentHeightOffset(commentRef.current?.offsetHeight)
		setCommentHeightClient(commentRef.current?.offsetHeight)
	}, [commentRef?.current?.offsetHeight])

	dayjs.locale(ru)
	dayjs.extend(relativeTime)

	return (
		<>
			<Box
				sx={{
					display: 'flex',
					height: '100%',
					'&:hover': { borderColor: 'gray' },
				}}>
				<Divider
					orientation='vertical'
					sx={{
						height: commentHeightOffset,
						pl: 1.3,
					}}
				/>
				<Box sx={{ px: 4.5, width: '100%' }}>
					<Box
						ref={commentRef}
						sx={{
							display: 'flex',
							alignItems: 'flex-start',
							postion: 'relative',
						}}>
						<Divider
							orientation='vertical'
							sx={{
								mr: 3,
								height: commentHeightClient ? commentHeightClient : 0,
							}}
						/>
						<Box
							sx={{
								display: 'flex',
								flexDirection: 'column',
								height: '100%',
							}}>
							<Box
								sx={{
									height: commentHeightOffset ? commentHeightOffset - 20 : 0,
									mr: 1,
								}}>
								<Avatar
									sx={{
										width: 20,
										height: 20,
										fontSize: 16,
										bgcolor: green[400],
										mb: 1,
									}}
									aria-label='recipe'
									src={comment?.user?.profile_image ?? ''}>
									{comment?.user?.profile_image
										? ''
										: comment?.user?.user_name[0].toUpperCase()}
								</Avatar>
							</Box>
						</Box>
						<Box sx={{ width: '100%' }}>
							<Box sx={{ display: 'flex' }}>
								<Typography sx={{ marginRight: 1 }} variant='caption'>
									{comment?.user?.user_name ?? 'Гость'}
								</Typography>

								<Typography sx={{ color: 'GrayText' }} variant='caption'>
									{dayjs(comment?.creation_date).toNow(true) + ' назад'}
								</Typography>
							</Box>
							{isEditing ? (
								<Box
									ref={editingBoxRef}
									sx={{
										mb: 2,
										pl: 4,
										display: 'flex',
										flexDirection: 'column',
										maxWidth: 600,
									}}>
									<Typography variant='caption' color={'GrayText'}>
										Вы отвечаете пользователю{' '}
										{'@' + comment?.user?.user_name ?? 'Гость'}
									</Typography>
									<TextareaAutosize
										minRows={2}
										onChange={(e) => setEditingCommentContent(e.target.value)}
										className='textarea'
										maxLength={320}
									/>
									<Box
										sx={{ display: 'flex', justifyContent: 'space-between' }}>
										<Button
											onClick={submitEditing}
											variant='outlined'
											sx={{ mt: 1, maxWidth: 220 }}>
											Оставить комментарий
										</Button>
										<Typography
											sx={{ userSelect: 'none' }}
											color={'ButtonHighlight'}
											variant='caption'>
											{editingCommentContent.length}/320
										</Typography>
									</Box>
								</Box>
							) : (
								<Typography className='comment' sx={{}} variant='body1'>
									{comment.comment}
								</Typography>
							)}
							<Box
								sx={{
									display: 'flex',
									alignItems: 'center',
								}}>
								<Button
									variant='text'
									sx={{ color: 'white', display: 'flex', alignItems: 'center' }}
									onClick={() => setIsCommenting((state) => (state = !state))}>
									<Comment sx={{ mr: 1, width: 20, height: 20 }} />
									<Typography sx={{ display: 'md: none', fontSize: 14 }}>
										Ответить
									</Typography>
								</Button>
								<IconButton
									id='more'
									aria-controls={moreDropdownOpen ? 'more options' : undefined}
									aria-haspopup='true'
									aria-expanded={moreDropdownOpen ? 'true' : undefined}
									onClick={handleClick}>
									<MoreHoriz sx={{ width: 16, height: 16 }} />
								</IconButton>
								<Menu
									id='more options'
									anchorEl={moreButtonEl}
									open={moreDropdownOpen}
									onClose={handleClose}>
									{comment?.user?.id === userDetails?.id && [
										<MenuItem
											onClick={handleClose}
											sx={{ width: '100%', height: 36 }}>
											<Box onClick={() => handleEditing()} className='flex'>
												<Edit sx={{ mr: 1 }} />
												<Typography>Редактировать</Typography>
											</Box>
										</MenuItem>,
										<MenuItem
											onClick={handleClose}
											sx={{ width: '100%', height: 36 }}>
											<FormControlLabel
												onClick={() =>
													handleDelete({ id: comment.id, model: 'comment' })
												}
												control={<Delete sx={{ mx: 1.2 }} />}
												label='Удалить'
											/>
										</MenuItem>,
									]}
									{comment.user.id !== userDetails?.id && (
										<MenuItem
											onClick={handleClose}
											sx={{ width: '100%', height: 36 }}>
											<FormControlLabel
												control={<Report sx={{ mx: 1.2 }} />}
												label='Пожаловаться'
											/>
										</MenuItem>
									)}
									<Divider />
									<MenuItem
										onClick={handleClose}
										sx={{ width: '100%', height: 36 }}>
										<FormControlLabel
											control={<Checkbox />}
											label='Включить уведомления'
										/>
									</MenuItem>
								</Menu>
							</Box>
						</Box>
					</Box>
					{isCommenting && (
						<Box sx={{ display: 'flex', width: '100%', position: 'relative' }}>
							<Divider
								orientation='vertical'
								sx={{
									height: commentHeightOffset ? commentHeightOffset + 62 : 0,
									position: 'absolute',
									left: -37,
								}}
							/>
							<Divider
								orientation='vertical'
								sx={{
									height: commentHeightOffset ? commentHeightOffset + 62 : 0,
								}}
							/>
							<Box sx={{ flex: '0 1 100%' }}>
								<AddComment
									parentComment={comment}
									answerData={answerData}
									isCommenting={isCommenting}
									setIsCommenting={setIsCommenting}
									profileData={userDetails}
								/>
							</Box>
						</Box>
					)}
				</Box>
			</Box>
		</>
	)
}
