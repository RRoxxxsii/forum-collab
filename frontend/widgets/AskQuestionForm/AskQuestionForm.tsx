'use client'
import { AskQuestionFormSubmit } from '@/features/AskQuestionFormSubmit'
import { AskQuestionFormTags } from '@/features/AskQuestionFormTags'
import { IChip } from '@/types/types'
import { Box, TextField } from '@mui/material'
import React, { useState } from 'react'
import { TiptapEditor } from '../TiptapEditor'

const tagsMock = [
	{ is_relevant: false, is_user_tag: true, tag: 'js', use_count: '224' },
	{ is_relevant: true, is_user_tag: false, tag: 'html', use_count: '123' },
	{ is_relevant: true, is_user_tag: false, tag: 'css', use_count: '12124' },
	{ is_relevant: true, is_user_tag: false, tag: 'react', use_count: '21' },
	{ is_relevant: true, is_user_tag: false, tag: 'django', use_count: '21' },
	{ is_relevant: true, is_user_tag: false, tag: 'test', use_count: '21' },
	{ is_relevant: true, is_user_tag: false, tag: 'lmao', use_count: '21' },
]

export const AskQuestionForm = ({}: {}) => {
	const [titleValue, setTitleValue] = useState('')
	const [questionContent, setQuestionContent] = useState('')
	const [tags, setTags] = useState<string[]>([])
	const [images, setImages] = useState<string[]>([])

	return (
		<>
			<TextField
				type='text'
				autoFocus
				autoComplete='off'
				fullWidth
				label='Тема вопроса'
				id='headline'
				sx={{ mb: 2 }}
				value={titleValue}
				onChange={(e) => setTitleValue(e.target.value)}
			/>
			<TiptapEditor
				questionContent={questionContent}
				setQuestionContent={setQuestionContent}
			/>
			<Box sx={questionFormBottom}>
				<AskQuestionFormTags
					tags={tagsMock}
					setTags={setTags}
					disabled={false}
					limit={5}
				/>
				<AskQuestionFormSubmit
					titleValue={titleValue}
					questionContent={questionContent}
					tags={tags}
					images={images}
				/>
			</Box>
		</>
	)
}

const questionFormBottom = {
	display: 'flex',
	alignItems: 'center',
	justifyContent: 'space-between',
}
