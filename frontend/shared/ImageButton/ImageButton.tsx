'use client'
import { useElementSize } from '@/lib/hooks/useElementSize'
import { Fullscreen, Remove } from '@mui/icons-material'
import { Box, IconButton, useMediaQuery } from '@mui/material'
import Image from 'next/image'
import { usePathname, useRouter, useSearchParams } from 'next/navigation'
import classes from './ImageButton.module.scss'
import { useContext } from 'react'
import { UserDeviceContext } from '@/providers/UserDeviceProvider'
interface ImageButtonProps {
	remove?: boolean
	fullscreen?: boolean
	imageUrl: string
	imageAlt: string
	handleRemove?: () => void
	onClick?: () => void
	width?: number | string
	height?: number | string
}

export const ImageButton = ({
	fullscreen = true,
	remove = false,
	imageUrl,
	imageAlt,
	onClick,
	handleRemove,
	height = '100%',
	width = '100%',
}: ImageButtonProps) => {
	const router = useRouter()
	const pathname = usePathname()
	const searchParams = useSearchParams()
	const { userDevice } = useContext(UserDeviceContext)

	const handleFullscreen = () => {
		const current = new URLSearchParams(Array.from(searchParams.entries()))

		current.set('image', imageUrl)
		// cast to string
		const search = current.toString()
		// or const query = `${'?'.repeat(search.length && 1)}${search}`;
		const query = search ? `?${search}` : ''

		router.push(`${pathname}${query}`)
	}
	const [BoxRef, { width: boxWidth, height: boxHeight }] = useElementSize()

	return (
		<div
			ref={BoxRef}
			style={{
				width:
					userDevice === 'mobile' && typeof width === 'number'
						? width / 2
						: width,
				height:
					userDevice === 'mobile' && typeof height === 'number'
						? height / 2
						: height,
			}}
			className={classes.ImageButton}>
			<Image
				height={boxHeight}
				width={boxWidth}
				src={imageUrl}
				alt={imageAlt}
				className='object-cover'
			/>
			<Box
				sx={{
					display: 'flex',
					position: 'absolute',
					top: '50%',
					left: '50%',
					transform: 'translate(-50%, -50%)',
				}}>
				{fullscreen && (
					<IconButton onClick={handleFullscreen} size='small'>
						<Fullscreen />
					</IconButton>
				)}
				{remove && (
					<IconButton onClick={handleRemove} size='small'>
						<Remove />
					</IconButton>
				)}
			</Box>
		</div>
	)
}
