'use client'
import { AskQuestionFormSubmit } from '@/features/AskQuestionFormSubmit'
import { AskQuestionFormTags } from '@/features/AskQuestionFormTags'
import { AskFastContext } from '@/providers/AskFastProvider'
import { ITag } from '@/types/types'
import { Box, TextField } from '@mui/material'
import { useSearchParams } from 'next/navigation'
import {
	Dispatch,
	SetStateAction,
	useContext,
	useEffect,
	useState,
} from 'react'
import { TiptapEditor } from '../TiptapEditor'
const fetchTagsOnQuery = async ({
	setTagsToDisplay,
	tagQuery,
}: {
	setTagsToDisplay: Dispatch<SetStateAction<ITag[]>>
	tagQuery: string
}) => {
	try {
		const response = await fetch(`/api/forum/ask-question?q=${tagQuery}`, {
			method: 'GET',
		})
		if (response.ok) {
			const dataObject = await response.json()
			const tagsToDisplayData: ITag[] = dataObject.data
			setTagsToDisplay(tagsToDisplayData)
		} else {
			const error = await response.json()
			console.log(error)
		}
	} catch (error) {
		console.log(error)
	}
}

export const AskQuestionForm = ({ type }: { type: 'create' | 'edit' }) => {
	const searchParams = useSearchParams()
	const editTitle = searchParams.get('title')
	const editContent = searchParams.get('content')
	const editTags = searchParams.get('tags')

	const [questionContent, setQuestionContent] = useState('')
	const [images, setImages] = useState<string[]>([])
	const { askFastValue } = useContext(AskFastContext)
	const [titleValue, setTitleValue] = useState(askFastValue ? askFastValue : '')

	const [selectedTags, setSelectedTags] = useState<string[]>([])
	const [tagQuery, setTagQuery] = useState<string>('')
	const [tagsToDisplay, setTagsToDisplay] = useState<ITag[]>([])

	console.log(editTitle, editContent, editTags)
	console.log(selectedTags)
	useEffect(() => {
		if (tagQuery !== '') {
			// Delay the fetch request by 300ms to avoid excessive requests
			const timerId = setTimeout(() => {
				fetchTagsOnQuery({ setTagsToDisplay, tagQuery })
			}, 300)

			// Clean up the timer if tagQuery changes again
			return () => clearTimeout(timerId)
		} else {
			// Clear tags when the query is empty
			setTagsToDisplay([])
		}
	}, [tagQuery])

	useEffect(() => {
		if (editTitle && editContent && editTags) {
			setTitleValue(editTitle)
			setQuestionContent(editContent)
			setSelectedTags((selectedTags) => [...selectedTags, editTags])
		}
	}, [])

	return (
		<>
			<TextField
				type='text'
				autoFocus
				autoComplete='off'
				fullWidth
				label='Тема вопроса'
				id='headline'
				sx={{ mb: 2 }}
				value={titleValue}
				onChange={(e) => setTitleValue(e.target.value)}
			/>
			<Box
				sx={{
					minHeight: 220,
					mb: 2,
				}}>
				<TiptapEditor
					type='question'
					content={questionContent}
					setContent={setQuestionContent}
				/>
			</Box>
			<Box>
				<AskQuestionFormTags
					tagQuery={tagQuery}
					setTagQuery={setTagQuery}
					tagsToDisplay={tagsToDisplay}
					setSelectedTags={setSelectedTags}
					selectedTags={selectedTags}
					disabled={false}
					limit={5}
				/>
				<AskQuestionFormSubmit
					type={type}
					titleValue={titleValue}
					questionContent={questionContent}
					tags={selectedTags}
					images={images}
				/>
			</Box>
		</>
	)
}
