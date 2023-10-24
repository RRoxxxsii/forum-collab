'use client'
import '@/shared/styles/EditorTextStyles.scss'
import { AddPhotoAlternate } from '@mui/icons-material'
import { Box, IconButton, Skeleton } from '@mui/material'
import { BubbleMenu, EditorContent, useEditor } from '@tiptap/react'
import Link from 'next/link'
import { Dispatch, SetStateAction, useEffect } from 'react'
import './styles.scss'
import { BubbleMenuContent } from './utils/BubbleMenuContent'
import { EditorExtensions } from './utils/Extensions'

const EditorContentValue = ``

export const TiptapEditor = ({
	content,
	setContent,
	type,
	contentOnEdit,
}: {
	type: 'question' | 'answer'
	content: string
	setContent: Dispatch<SetStateAction<string>>
	contentOnEdit?: string
}) => {
	const editor = useEditor({
		extensions: EditorExtensions,
		editorProps: {
			attributes: {
				class: `prose-text-field ${
					(type === 'question' && 'prose-text-field--question') ||
					(type === 'answer' && 'prose-text-field--answer')
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

	useEffect(() => {
		if (contentOnEdit) {
			editor?.commands.setContent(contentOnEdit)
			setContent(contentOnEdit)
		}
	}, [contentOnEdit])
	if (!editor) {
		return <Skeleton variant='rectangular' height={288} />
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
			{(type === 'question' || type === 'answer') && (
				<Box sx={{ height: 40, px: 1 }} border={'1px solid #343947'}>
					<IconButton sx={{ width: 36, height: 36, color: '#b7b8c4' }}>
						<Link href={'/ask/uploadimage'}>
							<AddPhotoAlternate />
						</Link>
					</IconButton>
				</Box>
			)}

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
