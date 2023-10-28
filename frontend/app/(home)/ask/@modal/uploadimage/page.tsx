'use client'
import { ModalComponent } from '@/shared/Modal'
import { CustomFile } from '@/types'
import { Delete, OpenInFull, UploadFile } from '@mui/icons-material'
import { Box, Tab, Tabs, Typography } from '@mui/material'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import React, { useEffect, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import './styles.scss'

export default function UploadImagePage() {
	const router = useRouter()

	const [value, setValue] = useState<number>(0)
	const [files, setFiles] = useState<CustomFile[]>([])

	const handleChange = (event: React.ChangeEvent<{}>, newValue: number) => {
		setValue(newValue)
	}
	const { getRootProps, getInputProps, isDragActive } = useDropzone({
		accept: { 'image/png': ['.png'] },
		onDrop: (acceptedFiles: File[]) => {
			const updatedFiles: CustomFile[] = acceptedFiles.map((file) => ({
				file,
				preview: URL.createObjectURL(file),
			}))

			if (files.length + updatedFiles.length <= 3) {
				setFiles([...files, ...updatedFiles])
			}
		},
	})

	const removeImage = (index: number) => {
		// Remove an image from the preview
		const updatedFiles = [...files]
		URL.revokeObjectURL(updatedFiles[index].preview)
		updatedFiles.splice(index, 1)
		setFiles(updatedFiles)
	}
	const openImage = ({
		file,
		photoId,
	}: {
		file: CustomFile
		photoId: number
	}) => {
		// Remove an image from the preview
		router.push(`/ask/uploadimage/photo/${photoId}`)
	}

	const handleClose = () => {
		router.back()
	}

	useEffect(() => {
		// Make sure to revoke the data URIs to avoid memory leaks
		return () => {
			files.forEach((file) => URL.revokeObjectURL(file.preview))
		}
	}, [files])

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
				<section className='container'>
					<Box
						sx={{ mb: 2 }}
						{...getRootProps({
							className:
								'dropzone h-80 max-w-60 min-w-20 flex justify-center items-center border border-slate-200 p-4 border-dashed max-w-20 cursor-pointer',
						})}>
						<input {...getInputProps()} />
						{isDragActive ? (
							<Typography>Drop file(s) here ...</Typography>
						) : (
							<Typography>
								Drag and drop file(s) here, or click to select files
							</Typography>
						)}
					</Box>
					<Typography>Загруженные фотографии ({files.length}/3)</Typography>
					<div className='mt-4 flex'>
						{files.map((file, index) => (
							<div
								className='max-h-32 w-24 overflow-hidden mr-2'
								key={file.file.name}>
								<div className='relative w-24 image-item'>
									<img
										className='max-h-24 max-w-24 rounded-sm aspect-square object-cover '
										src={file.preview}
										alt={file.file.name}></img>
									<button
										className='absolute hover:brightness-200'
										style={{
											transform: `translate(-50%, -50%)`,
											top: '50%',
											left: '35%',
										}}
										// onClick={() => openImage({ file: file, photoId: index })}
									>
										<Link
											href={{
												pathname: `uploadimage/photo/${index}`,
												query: {
													imageUrl: file.preview,
													imageName: file.file.name,
												},
											}}>
											<OpenInFull />
										</Link>
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
									{file.file.name}
								</Typography>
							</div>
						))}
					</div>
				</section>
			</div>
		</ModalComponent>
	)
}

const tab = {
	'font-size': { md: '12px', xl: 0 },
}
