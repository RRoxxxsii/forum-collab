'use client'

import { ModalComponent } from '@/shared/Modal'
import { useRouter } from 'next/navigation'
import { CustomFile } from '../../../page'
import { Typography } from '@mui/material'
import Image from 'next/image'

interface UploadImagePageProps {
	file: CustomFile
	photoId: number
}

export default function UploadImagePage({
	file,
	photoId,
}: UploadImagePageProps) {
	const router = useRouter()
	const handleClose = () => {
		router.push('/ask/uploadimage')
	}
	return (
		<ModalComponent handleClose={handleClose}>
			<Image alt={file.file.name} src={file.preview ?? ''} />
			<Typography>{file.file.name ?? ''}</Typography>
		</ModalComponent>
	)
}
