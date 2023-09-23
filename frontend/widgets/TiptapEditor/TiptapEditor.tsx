'use client'
import { AddPhotoAlternate } from '@mui/icons-material'
import { Box, IconButton } from '@mui/material'
import { BubbleMenu, EditorContent, useEditor } from '@tiptap/react'
import { Dispatch, SetStateAction } from 'react'
import './styles.scss'
import { BubbleMenuContent } from './utils/BubbleMenuContent'
import { EditorExtensions } from './utils/Extensions'

const EditorContentValue = ``

export const TiptapEditor = ({
	content,
	setContent,
	type,
}: {
	type: 'question' | 'answer' | 'reply'
	content: string
	setContent: Dispatch<SetStateAction<string>>
}) => {
	const editor = useEditor({
		extensions: EditorExtensions,
		editorProps: {
			attributes: {
				class: `prose-text-field ${
					(type === 'question' && 'prose-text-field--question') ||
					(type === 'answer' && 'prose-text-field--answer') ||
					(type === 'reply' && 'prose-text-field--reply')
				}`,
				content: EditorContentValue,
			},
		},
	})

	if (editor) {
		setContent(editor?.getHTML())
	}

	return (
		<Box sx={{ position: 'relative' }}>
			{editor && (
				<BubbleMenu
					className='bubble-menu'
					tippyOptions={{
						duration: 200,
						animation: 'shift-toward-subtle',
						moveTransition: 'transform 0.2s ease-in-out',
					}}
					editor={editor}>
					<BubbleMenuContent editor={editor} />
				</BubbleMenu>
			)}
			<Box border={'1px solid grey'}>
				<IconButton color='default'>
					<AddPhotoAlternate />
				</IconButton>
			</Box>
			<EditorContent
				style={{ height: '100%' }}
				onChange={(e) => setContent}
				value={content}
				className='editor'
				editor={editor}
			/>
		</Box>
	)
}
