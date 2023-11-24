'use client'

import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown'
import CheckIcon from '@mui/icons-material/Check'
import CodeIcon from '@mui/icons-material/Code'
import FormatBoldIcon from '@mui/icons-material/FormatBold'
import FormatClearIcon from '@mui/icons-material/FormatClear'
import FormatItalicIcon from '@mui/icons-material/FormatItalic'
import FormatListBulletedIcon from '@mui/icons-material/FormatListBulleted'
import FormatListNumberedIcon from '@mui/icons-material/FormatListNumbered'
import FormatStrikethroughIcon from '@mui/icons-material/FormatStrikethrough'
import {
	Box,
	Button,
	ClickAwayListener,
	Divider,
	Grow,
	IconButton,
	MenuList,
	Paper,
	Popper,
	Typography,
} from '@mui/material'
import { Editor } from '@tiptap/react'

import AddLinkIcon from '@mui/icons-material/AddLink'

import { EditorProps } from '@tiptap/pm/view'
import { useRef, useState } from 'react'

const options = ['Обычный текст', 'Нумерованный список', 'Маркированный список']

export const BubbleMenuContent = ({ editor }: { editor: Editor }) => {
	const [open, setOpen] = useState(false)
	const anchorRef = useRef<HTMLDivElement>(null)

	const handleToggle = () => {
		setOpen((prevOpen) => !prevOpen)
	}

	const handleClose = (event: Event) => {
		if (
			anchorRef.current &&
			anchorRef.current.contains(event.target as HTMLElement)
		) {
			return
		}

		setOpen(false)
	}

	const paragraphDropdown = () => {
		if (editor.isActive('heading', { level: 1 })) {
			return 'Heading 1'
		}
		if (editor.isActive('heading', { level: 2 })) {
			return 'Heading 2'
		}
		if (editor.isActive('heading', { level: 3 })) {
			return 'Heading 3'
		}
		if (editor.isActive('orderedList')) {
			return 'Numbered list'
		}
		if (editor.isActive('bulletList')) {
			return 'Bulleted list'
		}

		return 'Normal text'
	}

	const isOnlyParagraph =
		!editor.isActive('bulletList') &&
		!editor.isActive('orderedList') &&
		!editor.isActive('heading')

	//Link function
	const setLink = () => {
		const previousUrl = editor.getAttributes('link').href
		const url = window.prompt('URL', previousUrl)

		// cancelled
		if (url === null) {
			return
		}

		// empty
		if (url === '') {
			editor.chain().focus().extendMarkRange('link').unsetLink().run()

			return
		}
		// update link
		editor.chain().focus().extendMarkRange('link').setLink({ href: url }).run()
	}

	return (
		<Box sx={{ display: 'flex' }}>
			<Box ref={anchorRef}>
				<Button
					sx={{ height: 48, width: 160 }}
					aria-label='Обычный текст'
					onClick={handleToggle}>
					Обычный текст
					<ArrowDropDownIcon />
				</Button>
			</Box>
			<Popper
				sx={{
					zIndex: 1,
				}}
				open={open}
				anchorEl={anchorRef.current}
				role={undefined}
				transition
				disablePortal>
				{({ TransitionProps, placement }) => (
					<Grow
						{...TransitionProps}
						style={{
							transformOrigin: 'center top',
						}}>
						<Paper>
							<ClickAwayListener onClickAway={handleClose}>
								<MenuList autoFocusItem sx={{ width: 'auto' }}>
									<Button
										sx={{ display: 'flex', p: 2 }}
										onClick={() => {
											editor.chain().focus().toggleOrderedList().run()
										}}>
										<Box
											sx={{
												display: 'flex',
												justifyContent: 'space-between',
											}}>
											<FormatListNumberedIcon sx={{ mr: 1 }} />
											<Typography>Упорядоченный список</Typography>
										</Box>
										{editor.isActive('orderedList') && (
											<CheckIcon sx={{ ml: 2 }} />
										)}
									</Button>
									<Button
										sx={{ display: 'flex', p: 2 }}
										onClick={() => {
											editor.chain().focus().toggleBulletList().run()
										}}>
										<Box
											sx={{
												display: 'flex',
												justifyContent: 'start',
											}}>
											<FormatListBulletedIcon sx={{ mr: 1 }} />
											<Typography>Маркированный список</Typography>
										</Box>
										{editor.isActive('bulletList') && (
											<CheckIcon sx={{ ml: 2 }} />
										)}
									</Button>
								</MenuList>
							</ClickAwayListener>
						</Paper>
					</Grow>
				)}
			</Popper>
			<IconButton
				aria-label='жирный'
				sx={{
					opacity: editor.isActive('bold') ? '1' : '0.5',
					borderRadius: '0',
				}}
				onClick={() => editor?.chain().focus().toggleBold().run()}
				className={editor.isActive('bold') ? 'is-active' : ''}>
				<FormatBoldIcon />
			</IconButton>
			<IconButton
				sx={{
					opacity: editor.isActive('italic') ? '1' : '0.5',
					borderRadius: '0',
				}}
				aria-label='курсив'
				onClick={() => editor?.chain().focus().toggleItalic().run()}
				className={editor.isActive('italic') ? 'is-active' : ''}>
				<FormatItalicIcon />
			</IconButton>
			<IconButton
				sx={{
					opacity: editor.isActive('strike') ? '1' : '0.5',
					borderRadius: '0',
				}}
				aria-label='перечеркнутый'
				onClick={() => editor?.chain().focus().toggleStrike().run()}>
				<FormatStrikethroughIcon />
			</IconButton>
			<IconButton
				sx={{
					opacity: editor.isActive('code') ? '1' : '0.5',
					borderRadius: '0',
				}}
				aria-label='код'
				onClick={() => editor?.chain().focus().toggleCode().run()}
				className={editor.isActive('code') ? 'is-active' : ''}>
				<CodeIcon />
			</IconButton>
			<IconButton
				sx={{
					opacity: editor.isActive('link') ? '1' : '0.5',
					borderRadius: '0',
				}}
				aria-label='ссылка'
				onClick={setLink}>
				<AddLinkIcon />
			</IconButton>
			<Divider orientation='vertical' flexItem />
			<IconButton
				sx={{
					opacity: editor.isActive('clear') ? '1' : '0.5',
					borderRadius: '0',
				}}
				aria-label='clear'
				onClick={() =>
					editor.chain().focus().clearNodes().unsetAllMarks().run()
				}>
				<FormatClearIcon />
			</IconButton>
		</Box>
	)
}
export const editorProps: EditorProps<any> = {
	attributes: {
		class: 'm-2 focus:outline-none',
	},
}
