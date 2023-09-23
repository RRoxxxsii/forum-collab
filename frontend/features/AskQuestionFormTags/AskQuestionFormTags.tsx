'use client'

import { ITag } from '@/types/types'
import { Box, Chip, TextField } from '@mui/material'
import Autocomplete from '@mui/material/Autocomplete'
import { Dispatch, SetStateAction, useState } from 'react'

interface AskQuestionFormTagsProps {
	limit: number
	disabled: boolean
	setSelectedTags: Dispatch<SetStateAction<string[]>>
	selectedTags: string[],
	tagsToDisplay: ITag[],
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
		<Box>

			<Autocomplete
				multiple
				disabled={disabled || disableInput}
				id='question-tags'
				options={
					tagsToDisplay
				}
				//@ts-ignore tag could only be an ITag, so we turnoff ts here
				getOptionLabel={(tag: ITag) =>  `${tag.tag_name} (${tag.use_count})`}
				sx={{ width: 600 }}
				freeSolo
				renderTags={(option: readonly ITag[] | string[], getTagProps) =>
					option.map((tag: ITag | string) => (
						<Chip
							variant='outlined'
							label={typeof tag === 'string' ? tag : tag.tag_name}
							{...getTagProps({ index: typeof tag === 'string' ? tag.indexOf(tag) || 0 : tagsToDisplay?.indexOf(tag) || 0 })}
							disabled={disabled}
							key={typeof tag === 'string' ? tag : tag.tag_name}
						/>
					))
				}
				onChange={(_event: any, newValue: any[]) => {
					console.log(newValue)
					if (typeof newValue === 'string'){
						console.log(newValue)
						setSelectedTags(newValue)
					} else {
						setSelectedTags(newValue.map((tag: ITag) => tag.tag_name))
					}
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
