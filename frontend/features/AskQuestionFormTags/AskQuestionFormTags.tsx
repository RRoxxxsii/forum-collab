'use client'

import { useDebounce } from '@/hooks/useMobile/useDebounce'
import { Box, TextField } from '@mui/material'
import Autocomplete from '@mui/material/Autocomplete'
import React, { useEffect } from 'react'

export const AskQuestionFormTags = () => {
	const [value, setValue] = React.useState<any | null>(null)
	const [options, setOptions] = React.useState<any[]>([])
	const [inputValue, setInputValue] = React.useState<string>('')

	const fetchSuggestions = async (inputValue: string) => {
		await fetch('', {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' },
		})
	}

	const debouncedFetchSuggestions = useDebounce(fetchSuggestions, 1000) // Adjust the delay as needed

	useEffect(() => {
		debouncedFetchSuggestions(inputValue)
	}, [inputValue, debouncedFetchSuggestions])

	return (
		<Box>
			<Autocomplete
				id='tags'
				sx={{ width: 300 }}
				getOptionLabel={(option) =>
					typeof option === 'string' ? option : option.description
				}
				filterOptions={(x) => x}
				onInputChange={(event, newInputValue) => {
					setInputValue(newInputValue)
				}}
				onChange={(event: any, newValue: any | null) => {
					setOptions(newValue ? [newValue, ...options] : options)
					setValue(newValue)
				}}
				renderInput={(params) => (
					<TextField {...params} label='Выбрать теги' required fullWidth />
				)}
				autoComplete
				includeInputInList
				filterSelectedOptions
				value={value}
				options={options}
				noOptionsText='No tags'
				// renderOption={(props, option) => {
				// 	const matches =
				// 		option.structured_formatting.main_text_matched_substrings || []

				// 	const parts = parse(
				// 		option.structured_formatting.main_text,
				// 		matches.map((match: any) => [
				// 			match.offset,
				// 			match.offset + match.length,
				// 		])
				// 	)

				// 	return (
				// 		<li {...props}>
				// 			<Grid container alignItems='center'>
				// 				<Grid item sx={{ display: 'flex', width: 44 }}>
				// 					<LocationOnIcon sx={{ color: 'text.secondary' }} />
				// 				</Grid>
				// 				<Grid
				// 					item
				// 					sx={{ width: 'calc(100% - 44px)', wordWrap: 'break-word' }}>
				// 					{parts.map((part, index) => (
				// 						<Box
				// 							key={index}
				// 							component='span'
				// 							sx={{ fontWeight: part.highlight ? 'bold' : 'regular' }}>
				// 							{part.text}
				// 						</Box>
				// 					))}
				// 					<Typography variant='body2' color='text.secondary'>
				// 						{option.structured_formatting.secondary_text}
				// 					</Typography>
				// 				</Grid>
				// 			</Grid>
				// 		</li>
				// 	)
				// }}
			/>
		</Box>
	)
}
