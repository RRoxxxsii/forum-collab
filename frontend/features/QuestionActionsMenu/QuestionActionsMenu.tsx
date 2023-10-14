import { IQuestion, IUser } from '@/types/types'
import {
	Bookmark,
	BookmarkOutlined,
	Delete,
	Edit,
	MoreHoriz,
	Report,
	Share,
	ShareOutlined,
} from '@mui/icons-material'
import {
	Checkbox,
	Divider,
	FormControlLabel,
	IconButton,
	Menu,
	MenuItem,
	Typography,
} from '@mui/material'
import Link from 'next/link'
import { redirect } from 'next/navigation'
import React, { useState } from 'react'
import { toast } from 'react-toastify'

async function deleteQuestion({ question_id }: { question_id: number }) {
	if (!question_id) return null
	const questionToast = toast.loading('Удаление вопроса...')
	try {
		const response = await fetch('/api/forum/delete-question', {
			method: 'POST',
			body: JSON.stringify({
				id: question_id,
			}),
			headers: { 'Content-Type': 'application/json' },
		})

		const result = await response.json()

		if (!response.ok) {
			let errorMessage = ''
			if (result?.code) {
				errorMessage +=
					'Ваша текущая сессия истекла, попробуйте перезагрузить страницу '
			}

			toast.update(questionToast, {
				render:
					errorMessage.length > 0
						? errorMessage
						: 'Разорвана связь с сервером, проверьте подключение',
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
			return null
		}
		toast.update(questionToast, {
			render: result.message,
			type: 'success',
			isLoading: false,
			autoClose: 3000,
		})
		redirect('/')
	} catch (error: any | unknown) {
		toast.update(questionToast, {
			render: 'Разорвана связь с сервером, проверьте подключение',
			type: 'error',
			isLoading: false,
			autoClose: 3000,
		})
	}
}

export const QuestionActionsMenu = ({
	questionData,
	profileData,
}: {
	questionData: IQuestion
	profileData: IUser | null
}) => {
	const [moreButtonEl, setMoreButtonEl] = useState<HTMLElement | null>(null)

	const moreDropdownOpen = Boolean(moreButtonEl)
	const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
		setMoreButtonEl(event.currentTarget)
	}
	const handleClose = () => {
		setMoreButtonEl(null)
	}

	return (
		<>
			<FormControlLabel
				control={<Checkbox icon={<ShareOutlined />} checkedIcon={<Share />} />}
				label='Поделиться'
			/>
			<FormControlLabel
				control={
					<Checkbox icon={<BookmarkOutlined />} checkedIcon={<Bookmark />} />
				}
				label='Избранное'
			/>
			<IconButton
				id='more'
				aria-controls={moreDropdownOpen ? 'more options' : undefined}
				aria-haspopup='true'
				aria-expanded={moreDropdownOpen ? 'true' : undefined}
				onClick={handleClick}>
				<MoreHoriz />
			</IconButton>
			<Menu
				id='more options'
				anchorEl={moreButtonEl}
				open={moreDropdownOpen}
				onClose={handleClose}>
				{questionData.user.id === profileData?.id && (
					<>
						<MenuItem onClick={handleClose} sx={{ width: '100%', height: 36 }}>
							<Link
								href={{
									pathname: `/ask/edit`,
									query: {
										id: questionData.id,
									},
								}}
								className='flex'>
								<Edit sx={{ mr: 1 }} />
								<Typography>Редактировать</Typography>
							</Link>
						</MenuItem>
						<MenuItem onClick={handleClose} sx={{ width: '100%', height: 36 }}>
							<FormControlLabel
								onClick={() => deleteQuestion({ question_id: questionData.id })}
								control={<Delete sx={{ mx: 1.2 }} />}
								label='Удалить'
							/>
						</MenuItem>
					</>
				)}
				<MenuItem onClick={handleClose} sx={{ width: '100%', height: 36 }}>
					<FormControlLabel
						control={<Report sx={{ mx: 1.2 }} />}
						label='Пожаловаться'
					/>
				</MenuItem>
				<Divider />
				<MenuItem onClick={handleClose} sx={{ width: '100%', height: 36 }}>
					<FormControlLabel
						control={<Checkbox />}
						label='Включить уведомления'
					/>
				</MenuItem>
			</Menu>
		</>
	)
}
