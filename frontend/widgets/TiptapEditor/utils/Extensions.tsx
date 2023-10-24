import HighlightExtension, {
	HighlightOptions,
} from '@tiptap/extension-highlight'
import LinkExtension, { LinkOptions } from '@tiptap/extension-link'
import PlaceholderExtension, {
	PlaceholderOptions,
} from '@tiptap/extension-placeholder'
import TypographyExtension, {
	TypographyOptions,
} from '@tiptap/extension-typography'
import { Extension, Mark, Node } from '@tiptap/react'
import StarterKit, { StarterKitOptions } from '@tiptap/starter-kit'
import ImageExtension, { ImageOptions } from '@tiptap/extension-image'
export const EditorExtensions: (
	| Extension<StarterKitOptions, any>
	| Mark<HighlightOptions, any>
	| Mark<LinkOptions, any>
	| Extension<PlaceholderOptions, any>
	| Extension<TypographyOptions, any>
	| Node<ImageOptions, any>
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
	LinkExtension.configure({
		openOnClick: false,
	}),
	PlaceholderExtension.configure({
		placeholder: 'Вы сейчас здесь',
	}),
	ImageExtension,
]
