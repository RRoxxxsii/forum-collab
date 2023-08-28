'use client'
import { BubbleMenu, EditorContent, useEditor } from '@tiptap/react'
import { Dispatch, SetStateAction } from 'react'
import './styles.scss'
import { BubbleMenuContent } from './utils/BubbleMenuContent'
import { EditorExtensions } from './utils/Extensions'

const EditorContentValue = ``

export const TiptapEditor = ({
	questionContent,
	setQuestionContent,
}: {
	questionContent: string
	setQuestionContent: Dispatch<SetStateAction<string>>
}) => {
	const editor = useEditor({
		extensions: EditorExtensions,
		editorProps: {
			attributes: {
				class: `border-2 rounded-sm border-gray-400`,
			},
		},
		content: EditorContentValue,
	})
	if (editor) {
		setQuestionContent(editor?.getHTML())
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
				onChange={(e) => setQuestionContent}
				value={questionContent}
				className='editor'
				editor={editor}
			/>
		</>
	)
}
