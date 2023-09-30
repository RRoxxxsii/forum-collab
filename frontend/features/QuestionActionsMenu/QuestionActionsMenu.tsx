import {
	ShareOutlined,
	Share,
	BookmarkOutlined,
	Bookmark,
	MoreHoriz,
	Edit,
	Report,
} from '@mui/icons-material'
import {
	FormControlLabel,
	Checkbox,
	IconButton,
	Menu,
	MenuItem,
	Typography,
	Divider,
} from '@mui/material'
import Link from 'next/link'
import React, { useState } from 'react'

export const QuestionActionsMenu = () => {
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
				<MenuItem onClick={handleClose} sx={{ width: '100%', height: 36 }}>
					<Link href={`edit`} className='flex'>
						<Edit sx={{ mr: 1 }} />
						<Typography>Редактировать</Typography>
					</Link>
				</MenuItem>
				<MenuItem onClick={handleClose} sx={{ width: '100%', height: 36 }}>
					<Link href={`edit`} className='flex'>
						<Report sx={{ mr: 1 }} />
						<Typography>Пожаловаться</Typography>
					</Link>
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
