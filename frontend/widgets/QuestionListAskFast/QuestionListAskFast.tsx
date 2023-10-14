'use client'
import { Box, TextField, InputAdornment, IconButton } from '@mui/material'
import Link from 'next/link'
import React, { ChangeEventHandler, FormEvent, useContext } from 'react'
import AccountCircleIcon from '@mui/icons-material/AccountCircle'
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos'
import { AskFastContext } from '@/providers/AskFastProvider'
import { redirect, useRouter } from 'next/navigation'

export const QuestionListAskFast = () => {
	const { askFastValue, setAskFastValue } = useContext(AskFastContext)
	const router = useRouter()
	const handleAskInput = (value: string) => {
		setAskFastValue(value)
	}

	const handleAsk = (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault()
		router.push('/ask')
	}

	return (
		<Box sx={{ width: '100%', mb: 4 }}>
			<Box
				sx={{
					position: 'relative',
					width: 'clamp(300px, 100%, 1200px)',
					height: '100%',
					display: 'flex',
					alignItems: 'center',
				}}>
				<form className='w-full' onSubmit={handleAsk}>
					<TextField
						fullWidth
						id='input-with-icon-textfield'
						size='medium'
						variant='outlined'
						label='Задайте вопрос'
						value={askFastValue}
						onChange={(e) => handleAskInput(e.target.value)}
						InputProps={{
							startAdornment: (
								<InputAdornment position='start'>
									<AccountCircleIcon />
								</InputAdornment>
							),
							endAdornment: (
								<InputAdornment position='end'>
									<IconButton aria-label='Спросить'>
										<Link href={'/ask'}>
											<ArrowForwardIosIcon />
										</Link>
									</IconButton>
								</InputAdornment>
							),
						}}
					/>
				</form>
			</Box>
		</Box>
	)
}
