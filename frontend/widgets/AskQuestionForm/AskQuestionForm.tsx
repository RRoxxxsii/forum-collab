'use client'
import { Paper, TextField, Typography } from '@mui/material'
import { EditorProvider, extensions } from '@tiptap/react'
import { AskTabs } from '../AskTabs'
import { MenuBar, editorContent, editorExtensions, editorProps } from './Menu'

export const AskQuestionForm = () => {
	return (
		<>
			<TextField fullWidth label='Тема вопроса' id='headline' sx={{ mb: 2 }} />
			<Typography sx={{ mb: 2 }} component='h1'>
				Текст вопроса
			</Typography>
			<EditorProvider
				editorProps={editorProps}
				slotBefore={<MenuBar />}
				extensions={editorExtensions}
				content={editorContent}></EditorProvider>
		</>
	)
}
