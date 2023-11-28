'use client'
import { useDebounce } from '@/lib/hooks/useDebounce'
import { BASE_URL } from '@/shared/constants'
import { Search } from '@mui/icons-material'
import { InputAdornment, TextField } from '@mui/material'
import { useEffect, useState } from 'react'
import { toast } from 'react-toastify'

export const QuestionSearch = () => {
	const [searchValue, setSearchValue] = useState('')

	const debouncedValue = useDebounce(searchValue)

	const questionsQuery = async () => {
		try {
			const response = await fetch(
				BASE_URL + `/search/search?q=${debouncedValue}`
			)

			const result = await response.json()

			if (!response.ok) {
				throw new Error(result)
			}
		} catch (error) {
			if (typeof error === 'string') {
				toast.error(error)
			}
			if (error instanceof Error) {
				toast.error(error.message)
			}
		}
	}

	useEffect(() => {
		questionsQuery()
	}, [debouncedValue])

	return (
		<TextField
			sx={{ mb: 4 }}
			fullWidth
			value={searchValue}
			onChange={(e) => setSearchValue(() => e.target.value)}
			placeholder='Поиск'
			InputProps={{
				startAdornment: (
					<InputAdornment sx={{ mr: 1 }} position='end'>
						<Search />
						{/* <IconButton aria-label='toggle password visibility' edge='end'>
							<Search />
						</IconButton> */}
					</InputAdornment>
				),
			}}
		/>
	)
}
