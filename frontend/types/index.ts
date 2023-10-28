export interface ILinkType {
	text: string
	href: string
	icon: any
}

export interface IQuestion {
	id: number
	user: IUser
	title: string
	content: string
	is_solved: boolean
	answers: IAnswer[]
	creation_date: string
	updated_date: string
	images: string[]
	rating: IRating
	tags: ITag[]
	answers_amount: number
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
	user: IUser
	answer: string
	is_solving: boolean
	creation_date: string
	rating: IRating
	images: string[]
	comments: IComment[]
	uploaded_images: string[]
}

export interface IErrorRes {
	error: string
}

export interface IComment {
	id: number
	user: IUser
	comment: string
	creation_date: string
	question_answer: number
}

export interface IUser {
	id: number
	about: string
	user_name: string
	created: Date
	email: string
	email_confirmed: boolean
	is_active: boolean
	is_banned: boolean
	profile_image: null | string
}

export interface IRating {
	id: number
	like_amount: number
	dislike_amount: number
	is_disliked: boolean
	is_liked: boolean
	question: number
	users_liked: number[]
	users_disliked: number[]
}

export interface ICustomFile {
	file: File
	preview: string
}

export interface IChangeRating {
	id: number
	model: IModelType
	action: 'like' | 'dislike'
	checked?: boolean
}

export interface DBlockOptions {
	HTMLAttributes: Record<string, any>
}

export type IModelType = 'question' | 'answer' | 'comment'

export type CategoryType = 'best' | 'closed' | 'opened'

export type FetchStatusType = 'loading' | 'success' | 'error'

export type UserDetailsType = IUser | null
