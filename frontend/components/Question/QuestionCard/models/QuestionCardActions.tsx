'use client'

import { Transliterate } from '@/shared/utils/Transliterate'
import { IQuestion } from '@/types'
import TextsmsIcon from '@mui/icons-material/Textsms'
import { Box, Chip, Typography, styled } from '@mui/material'
import Link from 'next/link'

const ListItem = styled('li')(({ theme }) => ({
	margin: theme.spacing(0.5),
}))

export const QuestionCardActions = ({
	questionData,
}: {
	questionData: IQuestion
}) => {
	return (
		<Box
			sx={{
				display: 'flex',
				width: '100%',
				justifyContent: 'space-between',
				p: 0,
				mb: 1,
				alignItems: 'center',
			}}>
			<Box
				sx={{
					display: 'flex',
					justifyContent: 'flex-start',
					flexWrap: 'wrap',
					listStyle: 'none',
					m: 0,
					flex: '90%',
					width: '100%',
				}}
				component='ul'>
				{questionData?.tags.map((tag) => {
					return (
						<ListItem
							sx={{
								p: 0,
								mr: 1,
								cursor: 'pointer',
								flexWrap: 'nowrap',
							}}
							key={tag.tag_name}>
							<Link href={`/questions/?tags=${Transliterate(tag?.tag_name)}`}>
								<Chip
									label={tag.tag_name}
									sx={{
										background: '#292929',
										color: '#e1e1e1',
										'&:hover': { transition: 0.3, background: '#363636' },
									}}
								/>
							</Link>
						</ListItem>
					)
				})}
			</Box>
			<Box
				sx={{
					display: 'flex',
					flex: '10%',
					justifyContent: 'flex-end',
					alignItems: 'center',
				}}>
				<Typography sx={{}}>{questionData?.answers_amount}</Typography>
				<TextsmsIcon sx={{ m: 1 }} />
			</Box>
		</Box>
	)
}