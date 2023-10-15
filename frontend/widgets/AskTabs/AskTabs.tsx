'use client'
import { Box, Tab, Tabs } from '@mui/material'
import React, { useState } from 'react'

type questionTyped = 'Вопрос' | 'Опрос'

export const AskTabs = () => {
	const [questionType, setQuestionType] = useState<questionTyped>('Вопрос')

	const handleChange = (
		event: React.SyntheticEvent,
		newValue: questionTyped
	): void => {
		setQuestionType(newValue)
	}

	const tabs = [
		{ label: 'Создать вопрос', value: 'Вопрос' },
		// { label: 'Опрос', value: 'Опрос' },
	]

	return (
		<Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
			<Tabs
				value={questionType}
				aria-label='Изменить тип вопроса'
				onChange={handleChange}>
				{tabs.map((tab) => (
					<Tab key={tab.label} value={tab.value} label={tab.label} />
				))}
			</Tabs>
		</Box>
	)
}
