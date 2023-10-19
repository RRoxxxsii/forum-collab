'use client'
import { DeleteContent } from '@/shared/api/deleteContent'
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
import { useRouter } from 'next/navigation'
import React, { useState } from 'react'

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
	const router = useRouter()
	const handleDelete = () => {
		DeleteContent({
			id: questionData.id,
			model: 'question',
		}).then(() => router.push('/'))
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
