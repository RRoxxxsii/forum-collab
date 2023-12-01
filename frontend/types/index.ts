import { SvgIconTypeMap } from '@mui/material'
import { OverridableComponent } from '@mui/material/OverridableComponent'

export type ILinkTo =
	| 'Настройки'
	| 'Уведомления'
	| 'Профиль'
	| 'Выйти'
	| 'Войти'
	| 'Главная'
	| 'Вопросы'
	| 'Спросить'

export type IHref =
	| '/'
	| '/profile'
	| '/login'
	| '/register'
	| '/ask'
	| '/questions'
	| '/settings'
	| '?notifications=open'

export interface ILinkType {
	text: ILinkTo
	href: IHref
	icon: OverridableComponent<SvgIconTypeMap<{}, 'svg'>> & {
		muiName: string
	}
	action?: () => void
	session?: boolean
}

export interface INotifications {
	id: number
	level: string
	target_object_id: number
	action_obj_object_id: number
	text: string
	emailed: boolean
	unread: boolean
	creation_date: string // Assuming it's a date string
	sender: number
	receiver: number
	target_content_type: number
	action_obj_content_type: number
}

export interface IImage {
	alt_text: string
	id: number
	image: string
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
	images: IImage[]
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
	images: IImage[]
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
	email: string
	user_name: string
	about: string
	profile_image: null | string
	is_active: boolean
	is_banned: boolean
	email_confirmed: boolean
	created: Date
	amount_solved: number
	best_tags: ITag[]
	karma: number
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
	checked?: boolean | number
}

export interface DBlockOptions {
	HTMLAttributes: Record<string, any>
}

export type IModelType = 'question' | 'answer' | 'comment'

export type CategoryType = 'best' | 'closed' | 'opened'

export type FetchStatusType = 'loading' | 'success' | 'error'

export type UserDetailsType = IUser | null
