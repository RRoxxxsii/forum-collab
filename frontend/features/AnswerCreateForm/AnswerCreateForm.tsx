'use client'
import { BASE_URL } from '@/shared/constants'
import { TiptapEditor } from '@/widgets/TiptapEditor'
import { Typography, Button } from '@mui/material'
import React, { useState } from 'react'

export const AnswerCreateForm = ({ pageId }: { pageId: string }) => {
	const [answerContent, setAnswerContent] = useState<string>('')

	async function addAnswer() {
		try {
			const response = await fetch(`${BASE_URL}/forum/answer-question/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ question: pageId, answer: answerContent }),
			})
			if (response.ok) {
				const data = await response.json()
			} else {
			}
		} catch (error) {}
	}

	return (
		<>
			<Typography
				variant='caption'
				color={'GrayText'}
				sx={{ display: 'flex', alignItems: 'center' }}>
				Ответить на вопрос как,
				<Typography variant='caption' sx={{ ml: 1 }} color={'lightblue'}>
					Гость
				</Typography>
			</Typography>
			<TiptapEditor
				type='answer'
				content={answerContent}
				setContent={setAnswerContent}
			/>
			<Button
				sx={{ mt: 1, mb: 3, width: 220, height: 50 }}
				variant='outlined'
				onClick={addAnswer}>
				Ответить
			</Button>
		</>
	)
}
