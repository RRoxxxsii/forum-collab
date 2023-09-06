import { JSDocImplementsTag } from 'typescript'

export interface LinkType {
	text: string
	href: string
	icon: any
}

export interface IQuestion {
	id: number
	user: number
	title: string
	content: string
	is_solved: boolean
	answers: IAnswer[]
	creation_date: string
	images: string[] // Assuming these are image URLs
	rating: IRating
	tags: ITag[]
}

export interface ITag {
	tag_name: string
	use_count: string
	is_relevant: boolean
	is_user_tag: boolean
}

export interface IAnswer {
	id: number
	question: number
	user: number
	answer: string
	is_solving: boolean
	creation_date: string
	rating: IRating
	images: string[]
	comments: IComment[]
	uploaded_images: string[]
}

export interface IComment {
	id: number
	user: number
	comment: string
	creation_date: string
	question_answer: number
}

export interface IRating {
	id: number
	like_amount: number
	dislike_amount: number
	question: number
	users_liked: number[]
	// Add other properties for rating as needed
}
