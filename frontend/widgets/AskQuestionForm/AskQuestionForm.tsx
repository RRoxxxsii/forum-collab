'use client'
import { AskQuestionFormSubmit } from '@/features/AskQuestionFormSubmit'
import { AskQuestionFormTags } from '@/features/AskQuestionFormTags'
import { AskFastContext } from '@/providers/AskFastProvider'
import { fetchMe, fetchQuestion } from '@/shared/api/fetchData'
import { IQuestion, ITag, IUser } from '@/types/types'
import { Box, Skeleton, TextField, Typography } from '@mui/material'
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
	const pageId = searchParams.get('id')

	const { askFastValue } = useContext(AskFastContext)
	const [questionData, setQuestionData] = useState<IQuestion | null>(null)
	const [profileData, setProfileData] = useState<IUser | null>(null)
	const [questionContent, setQuestionContent] = useState('')
	const [images, setImages] = useState<string[]>([])
	const [titleValue, setTitleValue] = useState(askFastValue ? askFastValue : '')

	const [selectedTags, setSelectedTags] = useState<string[]>([])
	const [tagQuery, setTagQuery] = useState<string>('')
	const [tagsToDisplay, setTagsToDisplay] = useState<ITag[]>([])

	useEffect(() => {
		fetchQuestion({ id: pageId, setQuestionData: setQuestionData })
		fetchMe({ setProfileData: setProfileData })
	}, [])

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
		if (questionData) {
			setTitleValue(questionData.title)
			setQuestionContent(questionData.content)
			setSelectedTags((selectedTags) => [
				...selectedTags,
				...questionData.tags.map((tag) => tag.tag_name),
			])
		}
	}, [questionData])

	return (
		<>
			<TextField
				type='text'
				autoFocus
				autoComplete='off'
				fullWidth
				label='Тема вопроса'
				id='headline'
				value={titleValue}
				onChange={(e) => setTitleValue(e.target.value)}
				inputProps={{ maxLength: 255 }}
			/>
			<Typography
				textAlign={'end'}
				color={'slategray'}
				sx={{ width: '100%', display: 'block' }}
				variant='caption'>
				{titleValue.length}/255
			</Typography>
			<Box
				sx={{
					minHeight: 220,
					mb: 2,
				}}>
				<TiptapEditor
					type='question'
					content={questionContent}
					setContent={setQuestionContent}
					contentOnEdit={questionData?.content}
				/>
			</Box>
			<Box>
				<AskQuestionFormTags
					tagQuery={tagQuery}
					setTagQuery={setTagQuery}
					tagsToDisplay={tagsToDisplay}
					setSelectedTags={setSelectedTags}
					selectedTags={selectedTags}
					disabled={type === 'create' ? false : true}
					limit={5}
				/>
				{type === 'create' && (
					<AskQuestionFormSubmit
						type={type}
						titleValue={titleValue}
						questionContent={questionContent}
						tags={selectedTags}
						images={images}
						userId={profileData?.id}
						questionId={questionData?.id}
					/>
				)}

				{questionData && type === 'edit' && (
					<AskQuestionFormSubmit
						type={type}
						titleValue={titleValue}
						questionContent={questionContent}
						tags={selectedTags}
						images={images}
						userId={profileData?.id}
						questionId={questionData?.id}
					/>
				)}
			</Box>
		</>
	)
}
