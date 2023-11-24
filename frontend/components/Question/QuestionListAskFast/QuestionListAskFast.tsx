'use client'
import { AskFastContext } from '@/providers/AskFastProvider'
import AccountCircleIcon from '@mui/icons-material/AccountCircle'
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos'
import { Box, IconButton, InputAdornment, TextField } from '@mui/material'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { FormEvent, useContext } from 'react'

export const QuestionListAskFast = () => {
	const router = useRouter()

	const { askFastValue, setAskFastValue } = useContext(AskFastContext)

	const handleAsk = (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault()
		router.push('/ask')
	}

	const handleAskFastInput = (value: string) => {
		setAskFastValue(value)
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
						onChange={(e) => handleAskFastInput(e.target.value)}
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
