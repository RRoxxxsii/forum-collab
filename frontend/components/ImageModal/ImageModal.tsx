'use client'
import { useElementSize } from '@/lib/hooks/useElementSize'
import { ModalComponent } from '@/shared/Modal'
import { Typography, Paper } from '@mui/material'
import Image from 'next/image'
import { useSearchParams, useRouter } from 'next/navigation'
import { useState } from 'react'

export const ImageModal = ({
	imageUrl,
	alt = 'image',
}: {
	imageUrl?: string
	alt?: string
}) => {
	const imageUrlQuery = useSearchParams().get('image')
	const router = useRouter()

	const [value, setValue] = useState<number>(0)

	const handleClose = () => {
		router.back()
	}
	const [modalRef, { width: boxWidth, height: boxHeight }] = useElementSize()

	if (!imageUrlQuery) return null

	return (
		<ModalComponent handleClose={handleClose}>
			<div ref={modalRef} className='flex justify-center align-middle'>
				<Image width={400} height={400} alt={alt} src={imageUrlQuery}></Image>
			</div>
		</ModalComponent>
	)
}
