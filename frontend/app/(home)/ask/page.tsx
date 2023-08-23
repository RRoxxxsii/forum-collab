'use client'
import FormatBoldIcon from '@mui/icons-material/FormatBold'
import FormatClearIcon from '@mui/icons-material/FormatClear'
import FormatItalicIcon from '@mui/icons-material/FormatItalic'
import FormatStrikethroughIcon from '@mui/icons-material/FormatStrikethrough'
import CodeIcon from '@mui/icons-material/TextFields'
import {
	Box,
	Divider,
	IconButton,
	Paper,
	TextField,
	Typography,
} from '@mui/material'
import HighlightExtension, {
	HighlightOptions,
} from '@tiptap/extension-highlight'
import TypographyExtension, {
	TypographyOptions,
} from '@tiptap/extension-typography'
import { EditorProps } from '@tiptap/pm/view'
import {
	EditorProvider,
	Extension,
	Mark,
	useCurrentEditor,
} from '@tiptap/react'
import StarterKit, { StarterKitOptions } from '@tiptap/starter-kit'

export default function AskPage() {
	const extensions: (
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

	const editorProps: EditorProps<any> = {
		attributes: {
			class: 'backgroundColor: blue',
		},
	}

	const content = `
<h2>
  Hi there,
</h2>
`

	return (
		<Box className='flex min-h-screen items-start max-h-80 relative'>
			<Box sx={{ px: 3, width: '100%' }}>
				<Box>
					<Typography sx={{ mb: 2 }} component='h1'>
						Создать вопрос
					</Typography>
					<Paper
						elevation={2}
						variant={'elevation'}
						sx={{
							p: 2,
							position: 'relative',
							width: 'clamp(300px, 100%, 1200px)',
							height: '100%',
							minHeight: '400px',
							alignItems: 'center',
						}}>
						<TextField
							fullWidth
							label='Тема вопроса'
							id='headline'
							sx={{ mb: 2 }}
						/>
					<Typography sx={{ mb: 2 }} component='h1'>
						Создать вопрос
					</Typography>
						<EditorProvider
							editorProps={editorProps}
							slotBefore={<MenuBar />}
							extensions={extensions}
							content={content}></EditorProvider>
					</Paper>
				</Box>
			</Box>
		</Box>
	)
}

const MenuBar = () => {
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
