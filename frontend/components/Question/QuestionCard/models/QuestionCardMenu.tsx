'use client'
import { DeleteContent } from '@/shared/api/deleteContent'
import { IQuestion, IUser } from '@/types'
import {
	Bookmark,
	Delete,
	Edit,
	MoreHoriz,
	Report,
	Share,
} from '@mui/icons-material'
import {
	Box,
	Checkbox,
	Divider,
	FormControlLabel,
	IconButton,
	Menu,
	MenuItem,
	Typography,
} from '@mui/material'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import React, { useState } from 'react'
import { toast } from 'react-toastify'

export const QuestionCardMenu = ({
	questionData,
	profileData,
}: {
	questionData: IQuestion
	profileData?: IUser | null
}) => {
	const [moreButtonEl, setMoreButtonEl] = useState<HTMLElement | null>(null)

	const moreDropdownOpen = Boolean(moreButtonEl)
	const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
		setMoreButtonEl(event.currentTarget)
	}
	const handleClose = () => {
		setMoreButtonEl(null)
	}
	const router = useRouter()
	const handleDelete = () => {
		DeleteContent({
			id: questionData.id,
			model: 'question',
		}).then(() => router.push('/'))
	}
	const FavoriteHandler = async () => {
		try {
			const response = await fetch('/api/favourites/favourites-add/', {
				method: 'POST',
				body: JSON.stringify({ question: questionData.id }),
				headers: {
					'Content-Type': 'application/json',
				},
			})
			const result = await response.json()

			if (!response.ok) {
				throw new Error(result?.detail ?? 'Не удалось добавить в избранное')
			}

			toast.success('Вопрос добавлен в избранное')
		} catch (error) {
			if (error instanceof Error) {
				toast.error(error.message)
				return
			}
			if (typeof error === 'string') {
				toast.error(error)
				return
			}
		}
	}

	const shareHandler = () => {
		navigator.clipboard.writeText(window.location.href)
		toast('Сохранено в буфер обмена')
	}

	return (
		<Box sx={{ display: 'flex', alignItems: 'center' }}>
			<button
				className='flex mr-4 hover:bg-neutral-800 rounded-md p-2'
				onClick={shareHandler}>
				<Share sx={{ mr: 1 }} />
				<Typography>Поделиться</Typography>
			</button>
			<button
				className='flex mr-4 hover:bg-neutral-800 rounded-md p-2'
				onClick={FavoriteHandler}>
				<Bookmark sx={{ mr: 1 }} />
				<Typography>Избранное</Typography>
			</button>
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
				{questionData.user.id === profileData?.id && [
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
					</MenuItem>,
					<MenuItem onClick={handleClose} sx={{ width: '100%', height: 36 }}>
						<FormControlLabel
							onClick={handleDelete}
							control={<Delete sx={{ mx: 1.2 }} />}
							label='Удалить'
						/>
					</MenuItem>,
				]}
				{questionData.id !== profileData?.id && (
					<MenuItem onClick={handleClose} sx={{ width: '100%', height: 36 }}>
						<FormControlLabel
							control={<Report sx={{ mx: 1.2 }} />}
							label='Пожаловаться'
						/>
					</MenuItem>
				)}
				<Divider />
				<MenuItem onClick={handleClose} sx={{ width: '100%', height: 36 }}>
					<FormControlLabel
						control={<Checkbox />}
						label='Включить уведомления'
					/>
				</MenuItem>
			</Menu>
		</Box>
	)
}
