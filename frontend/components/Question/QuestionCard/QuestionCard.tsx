import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { Transliterate } from '@/shared/utils/Transliterate'
import { IChangeRating, IQuestion, ITag } from '@/types'
import { Box, Divider } from '@mui/material'
import Link from 'next/link'
import { useContext, useEffect, useState } from 'react'
import {
	QuestionCardActions,
	QuestionCardContent,
	QuestionCardMenu,
	QuestionCardRating,
} from './models'

export const QuestionCard = ({
	questionData,
	isCard,
}: {
	questionData: IQuestion
	isCard: boolean
}) => {
	const { userDetails } = useContext(UserDetailsContext)
	const [questionCardData, setQuestionCardData] = useState<IQuestion | null>(
		null
	)

	useEffect(() => {
		setQuestionCardData(questionData)
	})

	const handleQuestionRating = ({
		model,
		id,
		action,
		checked,
	}: IChangeRating) => {}

	return (
		<>
			<Box
				key={questionData.id}
				sx={{
					borderRadius: '12px',
					width: 'clamp(300px, 100%, 1200px)',
					transition: 'border-color 0.3s ease-in-out',
					'&:hover': { transition: 0.3, background: '#1b1b1b' },
					cursor: 'pointer',
					mb: 2,
					textDecoration: 'none',
					p: 0.8,
					filter: questionData.is_solved ? 'brightness(70%)' : 'none',
				}}>
				<Link
					href={`/question/${questionData.id}/${Transliterate(
						questionData.title
					)}/?tags=${questionData.tags.map((tag: ITag) =>
						Transliterate(tag.tag_name)
					)}`}
					className='flex hover:no-underline'>
					<QuestionCardRating
						model='question'
						questionData={questionCardData}
						profileData={userDetails}
						handleRating={handleQuestionRating}
					/>
					<Box sx={{ width: '100%', ml: 1, mt: 2 }}>
						<QuestionCardContent questionData={questionData} />
						<QuestionCardActions questionData={questionData} />
						<QuestionCardMenu isCard questionData={questionData} />
					</Box>
				</Link>
			</Box>
			<Divider sx={{ mb: 2 }} />
		</>
	)
}
