import { CommentList } from '@/components/Comment/CommentList/CommentList'
import { EditingBox } from '@/components/EditingBox'
import { IAnswer, IModelType, IQuestion, UserDetailsType } from '@/types'
import { Comment, Star } from '@mui/icons-material'
import { Avatar, Box, Button, Divider, Typography } from '@mui/material'
import { green } from '@mui/material/colors'
import dayjs from 'dayjs'
import ru from 'dayjs/locale/ru'
import relativeTime from 'dayjs/plugin/relativeTime'
import { Dispatch, SetStateAction, useEffect, useRef, useState } from 'react'
import { AnswerCardEditing, AnswerCardMore, AnswerCardRating } from './models'

interface AnswerCardProps {
	answerData: IAnswer
	questionData: IQuestion
	userDetails: UserDetailsType
	handleSolve: ({ answerId }: { answerId: number }) => void
	handleDelete: ({ id, model }: { id: number; model: IModelType }) => void
	setQuestionData: Dispatch<SetStateAction<IQuestion | null>>
	solved: boolean
}

export function AnswerCard({
	answerData,
	questionData,
	userDetails,
	handleSolve,
	handleDelete,
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

	const answerRef = useRef<null | HTMLElement>(null)

	const [answerHeight, setAnswerHeight] = useState<number | undefined>(0)
	useEffect(() => {
		setAnswerHeight(answerRef.current?.offsetHeight)
	}, [answerRef.current?.offsetHeight])

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
							height: answerHeight ? answerHeight - 36 : 0,
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
							sx={{ height: answerHeight ? answerHeight - 36 : 0 }}></Divider>
					</Box>
					<Box sx={{ width: '100%' }}>
						<Box sx={{ display: 'flex', ml: 1 }}>
							<Typography sx={{ marginRight: 1 }} variant='caption'>
								{answerData?.user?.user_name ?? 'Гость'}
							</Typography>
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
									handleDelete={handleDelete}
									setIsEditing={setIsEditing}
								/>
							</Box>
							{!questionData.is_solved &&
								questionData.user.id === userDetails?.id && (
									<Box sx={{ display: 'flex', alignItems: 'center' }}>
										<Button
											onClick={() => handleSolve({ answerId: answerData.id })}
											size='small'
											variant='outlined'>
											Отметить лучшим
										</Button>
									</Box>
								)}
						</Box>
					</Box>
				</Box>
				<AnswerCardEditing
					answerData={answerData}
					answerHeight={answerHeight}
					isCommenting={isCommenting}
					setIsCommenting={setIsCommenting}
					userDetails={userDetails}
				/>
				<CommentList answerData={answerData} handleDelete={handleDelete} />
			</Box>
		</>
	)
}
