import React from 'react'

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
