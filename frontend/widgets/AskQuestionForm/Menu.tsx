'use client'

import CodeIcon from '@mui/icons-material/Code'
import FormatBoldIcon from '@mui/icons-material/FormatBold'
import FormatClearIcon from '@mui/icons-material/FormatClear'
import FormatItalicIcon from '@mui/icons-material/FormatItalic'
import FormatStrikethroughIcon from '@mui/icons-material/FormatStrikethrough'
import { Box, Divider, IconButton } from '@mui/material'
import { useCurrentEditor } from '@tiptap/react'

import HighlightExtension, {
	HighlightOptions,
} from '@tiptap/extension-highlight'
import TypographyExtension, {
	TypographyOptions,
} from '@tiptap/extension-typography'
import { EditorProps } from '@tiptap/pm/view'
import {
	Extension,
	Mark
} from '@tiptap/react'
import StarterKit, { StarterKitOptions } from '@tiptap/starter-kit'

export const MenuBar = () => {
	const { editor } = useCurrentEditor()

	if (!editor) {
		return null
	}

	return (
		<Box
			sx={{
				display: 'flex',
				alignItems: 'center',
				width: 'fit-content',
				borderRadius: 1,
				mb: 2,
				border: (theme) => `1px solid ${theme.palette.divider}`,
			}}>
			<IconButton
				aria-label='bold'
				sx={{ opacity: '0.5', borderRadius: '0' }}
				onClick={() => editor?.chain().focus().toggleBold().run()}>
				<FormatBoldIcon />
			</IconButton>
			<IconButton
				sx={{ opacity: '0.5', borderRadius: '0' }}
				aria-label='italic'
				onClick={() => editor?.chain().focus().toggleItalic().run()}>
				<FormatItalicIcon />
			</IconButton>
			<IconButton
				sx={{ opacity: '0.5', borderRadius: '0' }}
				aria-label='strike'
				onClick={() => editor?.chain().focus().toggleStrike().run()}>
				<FormatStrikethroughIcon />
			</IconButton>
			<IconButton
				sx={{ opacity: '0.5', borderRadius: '0' }}
				aria-label='code'
				onClick={() => editor?.chain().focus().toggleCode().run()}>
				<CodeIcon />
			</IconButton>
			<Divider orientation='vertical' flexItem />
			<IconButton
				sx={{ opacity: '0.5', borderRadius: '0' }}
				aria-label='clear'
				onClick={() => editor?.chain().focus().clearNodes().run()}>
				<FormatClearIcon />
			</IconButton>
		</Box>
	)
}

export const editorExtensions: (
	| Extension<StarterKitOptions, any>
	| Mark<HighlightOptions, any>
	| Extension<TypographyOptions, any>
)[] = [
	StarterKit.configure({
		bulletList: {
			keepMarks: true,
			keepAttributes: false, // TODO : Making this as `false` becase marks are not preserved when I try to preserve attrs, awaiting a bit of help
		},
		orderedList: {
			keepMarks: true,
			keepAttributes: false, // TODO : Making this as `false` becase marks are not preserved when I try to preserve attrs, awaiting a bit of help
		},
	}),
	HighlightExtension,
	TypographyExtension,
]

export const editorProps: EditorProps<any> = {
	attributes: {
		class: '',
	},
}

export const editorContent = `
<h2>
  Hi there,
</h2>
`
