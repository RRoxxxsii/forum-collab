'use client'
import { ModalComponent } from '@/shared/Modal'
import { Delete, OpenInFull, UploadFile } from '@mui/icons-material'
import { Box, Tab, Tabs, Typography } from '@mui/material'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import React, { Dispatch, SetStateAction, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import './styles.scss'

export const UploadImage = ({
	model,
	images,
	setImages,
}: {
	model: 'question' | 'answer'
	images: File[]
	setImages: Dispatch<SetStateAction<File[]>>
}) => {
	const isOpen = useSearchParams().has('upload_image')
	const router = useRouter()

	const [value, setValue] = useState<number>(0)

	const handleChange = (event: React.ChangeEvent<{}>, newValue: number) => {
		setValue(newValue)
	}
	const { getRootProps, getInputProps, isDragActive } = useDropzone({
		accept: { 'image/png': ['.png', '.jpg', '.webp', '.svg', '.jpeg'] },
		onDrop: (acceptedFiles: File[]) => {
			if (images.length + acceptedFiles.length <= 3) {
				setImages([...images, ...acceptedFiles])
			}
		},
	})

	const removeImage = (index: number) => {
		// Remove an image from the preview
		const updatedFiles = [...images]
		updatedFiles.splice(index, 1)
		setImages(updatedFiles)
	}

	const handleClose = () => {
		router.back()
	}

	if (!isOpen) return null

	return (
		<ModalComponent handleClose={handleClose}>
			<div className='p-2'>
				<Typography variant='h5'>Добавление фото</Typography>
				<Tabs
					sx={{ mb: 2 }}
					value={value}
					onChange={handleChange}
					aria-label='basic tabs example'>
					<Tab icon={<UploadFile />} label='Загрузить с устройства' />
					{/* <Tab icon={<LinkIcon />} label='Загрузить по ссылке' /> */}
				</Tabs>
				<section>
					<Box
						sx={{
							mb: 2,
							height: 300,
							border: '1px dashed gray',
							cursor: 'pointer',
						}}
						{...getRootProps({
							className:
								'dropzone h-80 max-w-60 min-w-20 flex justify-center items-center border border-slate-200 p-4 border-dashed max-w-20 cursor-pointer',
						})}>
						<input {...getInputProps()} />
						{isDragActive ? (
							<Typography>Перетащите файл(ы) сюда...</Typography>
						) : (
							<Typography>
								Перетащите файл(ы) сюда или щелкните, чтобы выбрать файлы.
							</Typography>
						)}
					</Box>
					<Typography>Загруженные фотографии ({images.length}/3)</Typography>
					<div className='mt-4 flex'>
						{images.map((image, index) => (
							<Box
								sx={{ maxWidth: 140, mr: 2, overflow: 'hidden' }}
								key={image.name}>
								<div className='relative w-24 image-item'>
									<img
										className='h-24 w-24 rounded-sm aspect-square object-cover '
										src={URL.createObjectURL(image)}
										alt={image.name}></img>
									<button
										className='absolute hover:brightness-200'
										style={{
											transform: `translate(-50%, -50%)`,
											top: '50%',
											left: '35%',
										}}
										//</div>onClick={() => openImage({ file: file, photoId: index })}
									>
										{/* <Link
											href={{
												pathname:
													model === 'answer'
														? `/ask?upload_image&photo=${image.name}`
														: `/?upload_image&photo=${image.name}`,
												query: {
													imageUrl: URL.createObjectURL(image),
													imageName: image.name,
												},
											}}>
											<OpenInFull />
										</Link> */}
									</button>
									<button
										className='absolute hover:brightness-200'
										style={{
											transform: `translate(-50%, -50%)`,
											top: '50%',
											left: '65%',
										}}
										onClick={() => removeImage(index)}>
										<Delete />
									</button>
								</div>
								<Typography
									sx={{
										fontSize: '14px',
										textOverflow: 'ellipsis',
										whiteSpace: 'nowrap',
										overflow: 'hidden',
										width: '100%',
										display: 'block',
									}}>
									{image.name}
								</Typography>
							</Box>
						))}
					</div>
				</section>
			</div>
		</ModalComponent>
	)
}
