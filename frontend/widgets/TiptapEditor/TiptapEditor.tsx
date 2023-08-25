'use client'
import { BubbleMenu, Editor, EditorContent, useEditor } from '@tiptap/react'
import './styles.scss'
import { EditorExtensions } from './utils/Extensions'
import { BubbleMenuContent } from './utils/BubbleMenuContent'
import { useCallback } from 'react'

export const TiptapEditor = () => {
	const logContent = useCallback((e: Editor) => console.log(e.getJSON()), [])
	const editor = useEditor({
		extensions: EditorExtensions,
		editorProps: {
			attributes: {
				class: `border-2 rounded-sm border-gray-400`,
			},
		},
	})

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
			<EditorContent className='editor' editor={editor} />
		</>
	)
}
