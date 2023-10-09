import React from 'react'

export default async function Layout(props: {
	children: React.ReactNode
	photomodal: React.ReactNode
}) {
	return (
		<>
			{props.photomodal}
			{props.children}
		</>
	)
}
