import { IAnswer, IUser, IModelType } from '@/types'
import { MoreHoriz, Edit, Delete, Report } from '@mui/icons-material'
import {
	IconButton,
	Menu,
	MenuItem,
	Box,
	Typography,
	FormControlLabel,
	Divider,
	Checkbox,
} from '@mui/material'
import React, { SetStateAction, useState } from 'react'

export const AnswerCardMore = ({
	answerData,
	userDetails,
	handleDelete,
	isEditing,
	setIsEditing,
}: {
	answerData: IAnswer
	userDetails: IUser | null
	isEditing: boolean
	setIsEditing: React.Dispatch<SetStateAction<boolean>>
	handleDelete: ({ id, model }: { id: number; model: IModelType }) => void
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
					<MenuItem onClick={handleClose} sx={{ width: '100%', height: 36 }}>
						<Box onClick={() => setIsEditing(!isEditing)} className='flex'>
							<Edit sx={{ mr: 1 }} />
							<Typography>Редактировать</Typography>
						</Box>
					</MenuItem>,
					<MenuItem onClick={handleClose} sx={{ width: '100%', height: 36 }}>
						<FormControlLabel
							onClick={() =>
								handleDelete({ id: answerData.id, model: 'answer' })
							}
							control={<Delete sx={{ mx: 1.2 }} />}
							label='Удалить'
						/>
					</MenuItem>,
				]}
				{answerData?.user?.id !== userDetails?.id && (
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
		</>
	)
}
