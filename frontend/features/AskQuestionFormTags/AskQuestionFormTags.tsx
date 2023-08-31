'use client'

import { IChip } from '@/types/types'
import { Box, Chip, TextField } from '@mui/material'
import Autocomplete from '@mui/material/Autocomplete'
import { Dispatch, SetStateAction, useState } from 'react'

export const AskQuestionFormTags = ({
	limit,
	disabled,
	setTags,
	tags,
}: {
	limit: number
	disabled: boolean
	tags: IChip[]
	setTags: Dispatch<SetStateAction<string[]>>
}) => {
	const [value, setValue] = useState<any | null>(null)
	const [disableInput, setDisableInput] = useState<boolean>(
		value?.length >= limit
	)

	return (
		<Box>
			<Autocomplete
				multiple
				disabled={disabled || disableInput}
				id='question-tags'
				options={tags.map((chip) => chip.tag)}
				sx={{ width: 600 }}
				freeSolo
				renderTags={(option: readonly string[], getTagProps) =>
					option.map((chip: string, index: number) => (
						<Chip
							variant='outlined'
							label={chip}
							{...getTagProps({ index })}
							disabled={disabled}
							key={chip}
						/>
					))
				}
				onChange={(_event: any, newValue: any) => {
					setTags(newValue)
					setDisableInput(newValue.length >= limit)
				}}
				renderInput={(params) => (
					<TextField {...params} variant='outlined' label='Выбрать теги' />
				)}
			/>
		</Box>
	)
}
