import { ModalComponent } from '@/shared/Modal'
import { useRouter, useSearchParams } from 'next/navigation'

export default function NotificationModal() {
	const modalOpen = useSearchParams().has('notifications')

	const router = useRouter()

	const handleClose = () => {
		router.back()
	}

	return (
		<ModalComponent handleClose={handleClose}>
			<div>yep</div>
		</ModalComponent>
	)
}
