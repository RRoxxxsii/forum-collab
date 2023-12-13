import { Metadata } from 'next'
import React from 'react'

export const metadata: Metadata = {
	title: 'Задать вопрос',
	description: 'создание вопроса',
}
export default async function Layout(props: {
	children: React.ReactNode
	modal: React.ReactNode
}) {
	return (
		<>
			{props.modal}
			{props.children}
		</>
	)
}
