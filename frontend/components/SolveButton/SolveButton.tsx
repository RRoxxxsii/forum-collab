'use client'
import { Box, Button } from '@mui/material'
import React from 'react'
import { handleSolve } from '../Answer/AnswerList/utils/HandleSolve'

export const SolveButton = ({ answerId }: { answerId: number }) => {
	return (
		<Box sx={{ display: 'flex', alignItems: 'center' }}>
			<Button
				onClick={() => handleSolve({ answerId: answerId })}
				size='small'
				variant='outlined'>
				Отметить лучшим
			</Button>
		</Box>
	)
}
