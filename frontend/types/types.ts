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
