'use client'

import { ITag } from '@/types/types'
import { Box, Chip, TextField } from '@mui/material'
import Autocomplete from '@mui/material/Autocomplete'
import { Dispatch, SetStateAction, useState } from 'react'

interface AskQuestionFormTagsProps {
	limit: number
	disabled: boolean
	setSelectedTags: Dispatch<SetStateAction<string[]>>
	tagsToDisplay: ITag[]
	setTagQuery: Dispatch<SetStateAction<string>>
	tagQuery: string
}

export const AskQuestionFormTags = ({
	limit,
	disabled,
	setSelectedTags,
	tagsToDisplay,
	setTagQuery,
	tagQuery,
}: AskQuestionFormTagsProps) => {
	const [value, setValue] = useState<ITag[]>([])
	const [disableInput, setDisableInput] = useState(value.length >= limit)

	console.log(tagsToDisplay)

	return (
		<Box>
			<Autocomplete
				multiple
				disabled={disabled || disableInput}
				id='question-tags'
				options={
					tagsToDisplay?.map((tag) => `${tag.tag_name}`) ||
					[]
				}
				sx={{ width: 600 }}
				freeSolo
				renderTags={(option: readonly string[], getTagProps) =>
					option.map((tag: string) => (
						<Chip
							variant='outlined'
							label={tag}
							{...getTagProps({ index: tag?.indexOf(tag) || 0 })}
							disabled={disabled}
							key={tag}
						/>
					))
				}
				onChange={(_event: any, newValue: any) => {
					setSelectedTags((prevstate) => prevstate = newValue.map((tag: string) => tag))
					setDisableInput(newValue.length >= limit)
				}}
				renderInput={(params) => (
					<TextField
						{...params}
						variant='outlined'
						label='Выбрать теги'
						value={tagQuery}
						onChange={(e) => setTagQuery(e.target.value)}
					/>
				)}
			/>
		</Box>
	)
}
