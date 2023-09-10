'use client'
import { BubbleMenu, EditorContent, useEditor } from '@tiptap/react'
import { Dispatch, SetStateAction } from 'react'
import './styles.scss'
import { BubbleMenuContent } from './utils/BubbleMenuContent'
import { EditorExtensions } from './utils/Extensions'

const EditorContentValue = ``

export const TiptapEditor = ({
	height,
	content,
	setContent,
}: {
	height: number | string
	content: string
	setContent: Dispatch<SetStateAction<string>>
}) => {
	const editor = useEditor({
		extensions: EditorExtensions,
		editorProps: {
			attributes: {
				class: `border-2 rounded-sm border-gray-400 `,
			},
		},
		content: EditorContentValue,
	})
	if (editor) {
		setContent(editor?.getHTML())
	}

	return (
		<>
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
			<EditorContent
				style={{ minHeight: height, height: '100%' }}
				onChange={(e) => setContent}
				value={content}
				className='editor'
				editor={editor}
			/>
		</>
	)
}
