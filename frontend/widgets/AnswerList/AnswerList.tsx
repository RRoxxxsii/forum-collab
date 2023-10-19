'use client'
import { ChangeRatingProps } from '@/features/QuestionItemRating/QuestionItemRating'
import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { ChangeRating } from '@/shared/api/changeRating'
import { DeleteContent } from '@/shared/api/deleteContent'
import { IAnswer, IComment, IQuestion } from '@/types/types'
import {
	ArrowDownward,
	ArrowDownwardOutlined,
	ArrowUpward,
	ArrowUpwardOutlined,
	Comment,
	Delete,
	Edit,
	MoreHoriz,
	Report,
} from '@mui/icons-material'
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
	Typography,
} from '@mui/material'
import { green } from '@mui/material/colors'
import dayjs from 'dayjs'
import { useContext, useState } from 'react'
import { toast } from 'react-toastify'
import { AddComment } from '../AddComment'
import { TiptapEditor } from '../TiptapEditor'
import { AskQuestionFormSubmit } from '@/features/AskQuestionFormSubmit'
import { AskAnswerFormSubmit } from '@/features/AskAnswerFormSubmit'
export const AnswerList = ({ questionData }: { questionData: IQuestion }) => {
	return (
		<>
			{questionData.answers.map((answer) => (
				<AnswerCard key={answer.id} answerData={answer} />
			))}
		</>
	)
}

function AnswerCard({ answerData }: { answerData: IAnswer }) {
	const [isCommenting, setIsCommenting] = useState<boolean>(false)

	const { userDetails } = useContext(UserDetailsContext)

	const handleSolved = async () => {
		const solveToast = toast.loading('Обработка ответа...')
		try {
			const response = await fetch('/api/forum/mark-answer-solving', {
				method: 'POST',
				body: JSON.stringify({
					question_answer_id: answerData.id,
				}),
				headers: { 'Content-Type': 'application/json' },
			})

			const result = await response.json()

			if (!response.ok) {
				toast.update(solveToast, {
					render: result.error,
					type: 'error',
					isLoading: false,
					autoClose: 3000,
				})
				return null
			}

			toast.update(solveToast, {
				render: result.message,
				type: 'success',
				isLoading: false,
				autoClose: 3000,
			})
		} catch (error) {
			toast.update(solveToast, {
				render: 'Проблема подключения с сервером, повторите попытку позже',
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
		}
	}
	const [clientRating, setClientRating] = useState(0)
	const [checked, setChecked] = useState<null | number>(null)

	const handleRating = ({ id, model, action, checked }: ChangeRatingProps) => {
		ChangeRating({ id: id, model: model, action: action })
		if (checked) {
			setClientRating(action === 'like' ? 1 : -1)
			setChecked(action === 'like' ? 0 : 1)
		} else {
			setClientRating((clientRating) => (clientRating = 0))
			setChecked(null)
		}
	}

	const [moreButtonEl, setMoreButtonEl] = useState<HTMLElement | null>(null)

	const moreDropdownOpen = Boolean(moreButtonEl)
	const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
		setMoreButtonEl(event.currentTarget)
	}
	const handleClose = () => {
		setMoreButtonEl(null)
	}

	const [isEditing, setIsEditing] = useState(false)
	const [newContent, setNewContent] = useState<string>(answerData.answer)
	return (
		<>
			<Box sx={{ px: 3, py: 2, width: '100%' }}>
				<Box
					sx={{
						display: 'flex',
						alignItems: 'flex-start',
						position: 'relative',
					}}>
					<Box
						sx={{
							display: 'flex',
							flexDirection: 'column',
							alignItems: 'center',
							height: '80px',
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
							src={answerData?.user?.profile_image ?? ''}>
							{!answerData?.user?.profile_image &&
								answerData?.user?.user_name[0].toUpperCase()}
						</Avatar>
						<Divider orientation='vertical'></Divider>
					</Box>
					<Box sx={{ width: '100%' }}>
						<Box sx={{ display: 'flex', ml: 1 }}>
							<Typography sx={{ marginRight: 1 }} variant='caption'>
								{answerData?.user?.user_name ?? 'Гость'}
							</Typography>
							<Typography sx={{ color: 'GrayText' }} variant='caption'>
								{dayjs(answerData?.creation_date).format('DD-MM-YYYY')}
							</Typography>
						</Box>
						{isEditing && (
							<>
								<TiptapEditor
									setContent={setNewContent}
									content={newContent}
									contentOnEdit={answerData.answer}
									type='answer'
								/>
								<AskAnswerFormSubmit
									answerContent={answerData.answer}
									images={[]}
								/>
							</>
						)}
						{!isEditing && (
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
								{answerData.rating.like_amount -
									answerData.rating.dislike_amount +
									clientRating}
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
								<FormControlLabel
									control={
										<IconButton
											onClick={() =>
												setIsCommenting((state) => (state = !state))
											}
											sx={{ ml: 1, mr: 0.5 }}>
											<Comment />
										</IconButton>
									}
									label='Ответить'
								/>
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
									{answerData?.user?.id === userDetails?.id && (
										<>
											<MenuItem
												onClick={handleClose}
												sx={{ width: '100%', height: 36 }}>
												<Box
													onClick={() => setIsEditing(true)}
													className='flex'>
													<Edit sx={{ mr: 1 }} />
													<Typography>Редактировать</Typography>
												</Box>
											</MenuItem>
											<MenuItem
												onClick={handleClose}
												sx={{ width: '100%', height: 36 }}>
												<FormControlLabel
													onClick={() =>
														DeleteContent({
															id: answerData.id,
															model: 'answer',
														})
													}
													control={<Delete sx={{ mx: 1.2 }} />}
													label='Удалить'
												/>
											</MenuItem>
										</>
									)}
									<MenuItem
										onClick={handleClose}
										sx={{ width: '100%', height: 36 }}>
										<FormControlLabel
											control={<Report sx={{ mx: 1.2 }} />}
											label='Пожаловаться'
										/>
									</MenuItem>
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
							<Box sx={{ display: 'flex', alignItems: 'center' }}>
								<Button onClick={handleSolved} size='small' variant='outlined'>
									Отметить решающим
								</Button>
							</Box>
						</Box>
					</Box>
				</Box>
				{isCommenting && (
					<AddComment
						isCommenting={isCommenting}
						setIsCommenting={setIsCommenting}
						profileData={userDetails}
						answerData={answerData}
					/>
				)}
				{answerData.comments.map((comment) => (
					<CommentCard key={comment.id} comment={comment} />
				))}
			</Box>
		</>
	)
}

const CommentCard = ({ comment }: { comment: IComment }) => {
	return (
		<>
			<Box sx={{ display: 'flex' }}>
				<Box sx={{ px: 8, py: 1, width: '100%' }}>
					<Box
						sx={{
							display: 'flex',
							alignItems: 'flex-start',
							postion: 'relative',
						}}>
						<Box
							sx={{
								display: 'flex',
								flexDirection: 'column',
								height: '100%',
							}}>
							<Avatar
								sx={{
									width: 20,
									height: 20,
									fontSize: 16,
									bgcolor: green[400],
									marginRight: 1,
								}}
								aria-label='recipe'
								src={comment?.user?.profile_image ?? ''}>
								{comment?.user?.profile_image
									? ''
									: comment?.user?.user_name[0].toUpperCase()}
							</Avatar>
						</Box>
						<Box sx={{ width: '100%' }}>
							<Box sx={{ display: 'flex' }}>
								<Typography sx={{ marginRight: 1 }} variant='caption'>
									{comment?.user?.user_name ?? 'Гость'}
								</Typography>
								<Typography sx={{ color: 'GrayText' }} variant='caption'>
									{dayjs(comment?.creation_date).format('DD-MM-YYYY')}
								</Typography>
							</Box>
							<Typography className='comment' sx={{}} variant='body1'>
								{comment.comment}
							</Typography>
							<Box
								sx={{
									display: 'flex',
									alignItems: 'center',
								}}>
								<FormControlLabel
									sx={{ fontSize: 10 }}
									control={
										<IconButton sx={{ ml: 0.5, mr: 0 }}>
											<Comment sx={{ width: 16 }} />
										</IconButton>
									}
									label='Ответить'
								/>
								<IconButton>
									<MoreHoriz sx={{ width: 12, height: 12 }} />
								</IconButton>
							</Box>
						</Box>
					</Box>
				</Box>
			</Box>
		</>
	)
}
