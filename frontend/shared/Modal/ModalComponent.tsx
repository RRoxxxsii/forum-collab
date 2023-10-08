'use client'
import Box from '@mui/material/Box'
import Modal from '@mui/material/Modal'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import { useRouter } from 'next/navigation'

const style = {
	position: 'absolute' as 'absolute',
	top: '50%',
	left: '50%',
	transform: 'translate(-50%, -50%)',
	maxWidth: 800,
	width: '100%',
	minWidth: 280,
	bgcolor: 'background.paper',
	border: '2px solid #000',
	boxShadow: 24,
	p: 4,
}

interface ModalComponentProps {
	// open: boolean
	// handleOpen: () => void
	handleClose: () => void
	children: React.ReactNode
}

export const ModalComponent = ({
	// open,
	// handleOpen,
	handleClose,
	children,
}: ModalComponentProps) => {
	return (
		<Modal
			keepMounted
			onClose={handleClose}
			open={true}
			aria-labelledby='keep-mounted-modal-title'
			aria-describedby='keep-mounted-modal-description'>
			<Box sx={style}>{children}</Box>
		</Modal>
	)
}
