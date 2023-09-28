'use client'
import '@/shared/styles/EditorTextStyles.scss'
import { AddPhotoAlternate } from '@mui/icons-material'
import { Box, IconButton } from '@mui/material'
import { BubbleMenu, EditorContent, useEditor } from '@tiptap/react'
import Link from 'next/link'
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
			},
			handleDrop: function (view, event, slice, moved) {
				if (
					!moved &&
					event.dataTransfer &&
					event.dataTransfer.files &&
					event.dataTransfer.files[0]
				) {
					// if dropping external files
					let file = event.dataTransfer.files[0] // the dropped file
					let filesize = (file.size / 1024 / 1024).toFixed(4) // get the filesize in MB
					if (
						(file.type === 'image/jpeg' || file.type === 'image/png') &&
						Number(filesize) < 10
					) {
						// check valid image type under 10MB
						// check the dimensions
						let image = new Image() // Create a new Image object
						image.src = URL.createObjectURL(file) // Set the image source to the dropped file

						image.onload = function () {
							// Wait for the image to load
							const { schema } = view.state
							const coordinates = view.posAtCoords({
								left: event.clientX,
								top: event.clientY,
							})
							const node = schema.nodes.image.create({
								src: image.src, // Use the image source as the image URL
							})
							const transaction = view.state.tr.insert(
								coordinates?.pos || 0,
								node
							)
							view.dispatch(transaction)
						}
					} else {
						window.alert(
							'Images need to be in jpg or png format and less than 10mb in size.'
						)
					}
					return true // handled
				}
				return false // not handled, use default behavior
			},
		},
		content: EditorContentValue,
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
			{type === 'question' ||
				(type === 'answer' && (
					<Box border={'1px solid #343947'}>
						<IconButton sx={{ color: '#b7b8c4' }}>
							<Link href={'addimage'}>
								<AddPhotoAlternate />
							</Link>
						</IconButton>
					</Box>
				))}

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
