'use client'

import { ModalComponent } from '@/shared/Modal'
import { Typography } from '@mui/material'
import Image from 'next/image'
import { useParams, useRouter, useSearchParams } from 'next/navigation'

export default function UploadImagePage() {
	const searchParams = useSearchParams()
	const router = useRouter()

	const imageUrl = searchParams.get('imageUrl')
	const imageName = searchParams.get('imageName')
	const handleClose = () => {
		router.back()
	}

	return (
		<ModalComponent handleClose={handleClose}>
			<Image
				width={300}
				height={300}
				alt={imageUrl ?? ''}
				src={imageName ?? ''}
			/>
			<Typography>{imageName ?? ''}</Typography>
			<Typography>dadad</Typography>
		</ModalComponent>
	)
}
