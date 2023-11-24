'use client'
import { useSearchParams } from 'next/navigation'
import React, { useEffect, useRef } from 'react'

interface AddImageModalProps {
	onClose: () => void
	children: React.ReactNode
}

export const AddImageModal = ({ onClose, children }: AddImageModalProps) => {
	const searchParams = useSearchParams()
	const modalRef = useRef<null | HTMLDialogElement>(null)
	const showModal = searchParams.get('modal')

	useEffect(() => {
		if (showModal === 'true') {
			modalRef.current?.showModal()
		} else {
			modalRef.current?.close()
		}
	}, [showModal])

	const closeModal = () => {
		modalRef.current?.close()
		onClose()
	}

	return <div></div>
}
