import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { ChangeRating } from '@/shared/api/changeRating'
import { IAnswer, IChangeRating, IModelType, IQuestion } from '@/types'
import { AddComment } from '@/widgets/AddComment'
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
import React, {
	Dispatch,
	SetStateAction,
	useContext,
	useEffect,
	useState,
} from 'react'
import { CommentCard } from '../CommentCard'
import { EditingBox } from '../EditingBox'
import {} from '../QuestionItemRating/QuestionItemRating'

interface AnswerCardProps {
	answerData: IAnswer
	handleSolve: ({ answerId }: { answerId: number }) => void
	handleDelete: ({ id, model }: { id: number; model: IModelType }) => void
	setQuestionData: Dispatch<SetStateAction<IQuestion | null>>
}

export function AnswerCard({
	answerData,
	handleSolve,
	handleDelete,
	setQuestionData,
}: AnswerCardProps) {
	const { userDetails } = useContext(UserDetailsContext)

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

	useEffect(() => {
		if (answerData.rating.is_liked) {
			setChecked(0)
		}
		if (answerData.rating.is_disliked) {
			setChecked(1)
		}
	}, [])

	const [editingContent, setEditingContent] = useState<string>(
		answerData.answer
	)

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
								<Button
									variant='text'
									sx={{ color: 'white' }}
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
									{answerData?.user?.id === userDetails?.id && [
										<MenuItem
											onClick={handleClose}
											sx={{ width: '100%', height: 36 }}>
											<Box
												onClick={() => setIsEditing(!isEditing)}
												className='flex'>
												<Edit sx={{ mr: 1 }} />
												<Typography>Редактировать</Typography>
											</Box>
										</MenuItem>,
										<MenuItem
											onClick={handleClose}
											sx={{ width: '100%', height: 36 }}>
											<FormControlLabel
												onClick={() =>
													handleDelete({ id: answerData.id, model: 'answer' })
												}
												control={<Delete sx={{ mx: 1.2 }} />}
												label='Удалить'
											/>
										</MenuItem>,
									]}
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
								<Button
									onClick={() => handleSolve({ answerId: answerData.id })}
									size='small'
									variant='outlined'>
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
					<CommentCard
						key={comment.id + comment.creation_date}
						comment={comment}
						answerData={answerData}
						handleDelete={handleDelete}
					/>
				))}
			</Box>
		</>
	)
}
