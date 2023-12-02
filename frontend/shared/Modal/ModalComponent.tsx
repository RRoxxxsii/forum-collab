'use client'
import Box from '@mui/material/Box'
import Modal from '@mui/material/Modal'

const style = {
	position: 'absolute' as 'absolute',
	top: '50%',
	left: '50%',
	transform: 'translate(-50%, -50%)',
	maxWidth: 800,
	width: '100%',
	minWidth: 280,
	bgcolor: 'background.paper',
	boxShadow: 24,
	p: 4,
}

interface ModalComponentProps {
	handleClose: () => void
	children: React.ReactNode
}

export const ModalComponent = ({
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
