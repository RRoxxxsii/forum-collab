import { JSDocImplementsTag } from 'typescript'

export interface IUser {
	id: string
	avatar: string
	username: string
	email: string
}

export interface IChip {
	tag: string
	use_count: string
	is_relevant: boolean
	is_user_tag: boolean
}

export interface IReply {
	id: string
	user: IUser
	content: string
	rating: number
	commentBranch: IComment[]
}

export interface IComment {
	id: string
	user: IUser
	content: string
	commentBranch: IComment[]
}
export interface IQuestionItem {
	id: string
	user: IUser
	title: string
	description: string
	comments?: IComment[]
	replies?: IReply[]
	chips: IChip[]
}

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

interface IAnswer {
	id: number
	// Add other properties for answers as needed
}

export interface IRating {
	id: number
	like_amount: number
	dislike_amount: number
	question: number
	users_liked: number[]
	// Add other properties for rating as needed
}
