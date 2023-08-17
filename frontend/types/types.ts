export interface IUser {
	id: string
	avatar: string
	username: string
	email: string
}

export interface IChip {
	key: number
	label: string
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
