import { CommentList } from '@/components/Comment/CommentList/CommentList'
import { EditingBox } from '@/components/EditingBox'
import { IAnswer, IQuestion, UserDetailsType } from '@/types'
import { Comment, Star } from '@mui/icons-material'
import { Avatar, Box, Button, Divider, Typography } from '@mui/material'
import { green } from '@mui/material/colors'
import dayjs from 'dayjs'
import ru from 'dayjs/locale/ru'
import relativeTime from 'dayjs/plugin/relativeTime'
import { Dispatch, SetStateAction, useEffect, useRef, useState } from 'react'

import Link from 'next/link'
import { AnswerCardEditing, AnswerCardMore, AnswerCardRating } from './models'
import { useElementSize } from '@/lib/hooks/useElementSize'
import { SolveButton } from '@/components/SolveButton'
import { useMediaQuery } from '@/lib/hooks/useMediaQuery'
import { ImageButton } from '@/shared/ImageButton'

interface AnswerCardProps {
	answerData: IAnswer
	questionData: IQuestion
	userDetails: UserDetailsType
	setQuestionData: Dispatch<SetStateAction<IQuestion | null>>
	solved: boolean
}

export function AnswerCard({
	answerData,
	questionData,
	userDetails,
	setQuestionData,
	solved,
}: AnswerCardProps) {
	const [isCommenting, setIsCommenting] = useState<boolean>(false)
	const [isEditing, setIsEditing] = useState(false)

	const [editingContent, setEditingContent] = useState<string>(
		answerData.answer
	)
	dayjs.locale(ru)
	dayjs.extend(relativeTime)

	const [answerRef, { width: answerWidth, height: answerHeight }] =
		useElementSize()

	return (
		<>
			<Box
				sx={{
					p: 2,
					width: '100%',
					borderLeft: solved ? '1px solid rgb(104, 130, 177)' : '',
				}}>
				{solved && (
					<>
						<Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
							<Star sx={{ mr: 1 }} />
							<Typography
								sx={{
									fontSize: 20,
								}}>
								Лучший ответ
							</Typography>
						</Box>
					</>
				)}
				<Box
					ref={answerRef}
					sx={{
						display: 'flex',
						alignItems: 'flex-start',
						position: 'relative',
						'&:hover': { borderColor: 'gray' },
					}}>
					<Box
						sx={{
							display: 'flex',
							flexDirection: 'column',
							alignItems: 'center',
							mr: 1,
							height: answerHeight ? answerHeight : 0,
						}}>
						<Avatar
							sx={{
								width: 20,
								height: 20,
								fontSize: 16,
								bgcolor: green[400],
								mb: 2,
							}}
							aria-label='recipe'
							src={answerData?.user?.profile_image ?? ''}>
							{!answerData?.user?.profile_image &&
								answerData?.user?.user_name[0].toUpperCase()}
						</Avatar>
						<Divider
							orientation='vertical'
							sx={{ height: answerHeight ? answerHeight - 37 : 0 }}></Divider>
					</Box>
					<Box sx={{ width: '100%' }}>
						<Box sx={{ display: 'flex', ml: 1 }}>
							{answerData?.user?.user_name ? (
								<Link
									href={`/profile/${answerData.user.id}`}
									className='text-xs mr-1'>
									{answerData?.user.user_name}
								</Link>
							) : (
								<Typography sx={{ marginRight: 1 }} variant='caption'>
									Гость
								</Typography>
							)}
							<Typography sx={{ color: 'GrayText' }} variant='caption'>
								{dayjs(answerData?.creation_date).toNow(true) + ' назад'}
							</Typography>
						</Box>
						{isEditing ? (
							<EditingBox
								newContent={editingContent}
								setNewContent={setEditingContent}
								isEditing={isEditing}
								setIsEditing={setIsEditing}
								answerData={answerData}
							/>
						) : editingContent ? (
							<Typography
								className='comment'
								sx={{ ml: 1 }}
								dangerouslySetInnerHTML={{ __html: editingContent }}
								variant='body1'
							/>
						) : (
							<Typography
								className='comment'
								sx={{ ml: 1 }}
								dangerouslySetInnerHTML={{ __html: answerData?.answer }}
								variant='body1'
							/>
						)}
						<Box>
							{answerData?.images?.map((image) => (
								<ImageButton
									width={128}
									height={128}
									imageUrl={image.image}
									imageAlt={image.alt_text}
								/>
							))}
						</Box>
						<Box
							sx={{
								display: 'flex',
								alignItems: 'center',
								justifyContent: 'space-between',
							}}>
							<Box sx={{ display: 'flex', alignItems: 'center' }}>
								<AnswerCardRating
									answerData={answerData}
									userDetails={userDetails}
								/>
								<Button
									variant='text'
									sx={{ color: 'white' }}
									onClick={() => setIsCommenting((state) => (state = !state))}>
									<Comment sx={{ mr: 1, width: 20, height: 20 }} />
									<Typography sx={{ display: 'md: none', fontSize: 14 }}>
										Ответить
									</Typography>
								</Button>
								<AnswerCardMore
									isEditing={isEditing}
									answerData={answerData}
									userDetails={userDetails}
									// handleDelete={handleDelete}
									setIsEditing={setIsEditing}
								/>
							</Box>
							{!questionData.is_solved &&
								questionData.user.id === userDetails?.id && (
									<SolveButton answerId={answerData.id} />
								)}
						</Box>
					</Box>
				</Box>
				<AnswerCardEditing
					answerData={answerData}
					isCommenting={isCommenting}
					setIsCommenting={setIsCommenting}
					userDetails={userDetails}
				/>
				<CommentList answerData={answerData} />
			</Box>
		</>
	)
}
