'use client'

import { ITag } from '@/types/types'
import { Box, Chip, TextField } from '@mui/material'
import Autocomplete from '@mui/material/Autocomplete'
import { Dispatch, SetStateAction, useState } from 'react'

interface AskQuestionFormTagsProps {
	limit: number
	disabled: boolean
	setSelectedTags: Dispatch<SetStateAction<string[]>>
	selectedTags: string[]
	tagsToDisplay: ITag[]
	setTagQuery: Dispatch<SetStateAction<string>>
	tagQuery: string
}

export const AskQuestionFormTags = ({
	limit,
	disabled,
	setSelectedTags,
	selectedTags,
	tagsToDisplay,
	setTagQuery,
	tagQuery,
}: AskQuestionFormTagsProps) => {
	const [disableInput, setDisableInput] = useState(selectedTags.length >= limit)

	return (
		<Box sx={{ maxWidth: 600, width: '100%', mr: 2, mb: 2 }}>
			<Autocomplete
				multiple
				disabled={disabled || disableInput}
				id='question-tags'
				options={tagsToDisplay}
				value={selectedTags}
				//@ts-ignore tag could only be an ITag, so we turnoff ts here
				getOptionLabel={(tag: ITag) => `${tag.tag_name} (${tag.use_count})`}
				sx={{ width: '100%' }}
				freeSolo
				renderTags={(option: readonly ITag[] | string[], getTagProps) =>
					option.map((tag: ITag | string, index: number) => (
						<Chip
							variant='outlined'
							label={typeof tag === 'string' ? tag : tag.tag_name}
							{...getTagProps({
								index: index,
							})}
							disabled={disabled}
							key={typeof tag === 'string' ? tag : tag.tag_name}
						/>
					))
				}
				onChange={(
					_event: React.SyntheticEvent,
					newValue: (string | ITag)[]
				) => {
					const selectedValues = newValue.map((value) =>
						typeof value === 'string' ? value : value.tag_name
					)
					setSelectedTags(selectedValues)
					setDisableInput(selectedValues.length >= limit)
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
