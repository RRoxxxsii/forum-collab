'use client'
import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import {
	Button,
	Dialog,
	DialogActions,
	DialogContent,
	DialogContentText,
	DialogTitle,
} from '@mui/material'
import { redirect } from 'next/navigation'

import { useContext, useEffect, useState } from 'react'
import { toast } from 'react-toastify'

export const AccountDeletion = () => {
	const { setUserDetails, userDetails } = useContext(UserDetailsContext)

	const handleDelete = async () => {
		try {
			const response = await fetch('/api/account/delete-account', {
				method: 'GET',
			})

			const result = await response.json()

			if (!response.ok) {
				throw new Error(result)
			}
			setUserDetails(null)
			toast.success('Аккаунт успешно удален')
			toggleModal()
			redirect('/')
		} catch (error) {
			if (typeof error === 'string') {
				toast.error(error)
			}
			if (error instanceof Error) {
				toast.error(error.message)
			}
		}
	}

	const [deleteModalOpen, setDeleteModalOpen] = useState(false)
	const [timer, setTimer] = useState(5)
	const toggleModal = () => {
		setDeleteModalOpen((prev) => !prev)
	}

	useEffect(() => {
		if (!deleteModalOpen) {
			setTimer(5)
		} else {
			setInterval(() => {
				if (timer >= 0) {
					setTimer((timer) => timer - 1)
				}
			}, 1000)
		}
		return () => {
			setTimer(5)
		}
	}, [deleteModalOpen])

	return (
		<>
			<Dialog
				color='warning'
				open={deleteModalOpen}
				onClose={toggleModal}
				aria-labelledby='alert-dialog-title'
				aria-describedby='alert-dialog-description'>
				<DialogTitle id='alert-dialog-title'>
					Вы действительно хотите удалить аккаунт?
				</DialogTitle>
				<DialogContent>
					<DialogContentText id='alert-dialog-description'>
						Аккаунт можно будет восстановить в течение 31 дней с момента
						удаления
					</DialogContentText>
				</DialogContent>
				<DialogActions>
					<Button disabled={timer >= 0} onClick={handleDelete}>
						{timer >= 0 ? `(${timer}) ` : ''}Продолжить
					</Button>
					<Button onClick={toggleModal}>Отмена</Button>
				</DialogActions>
			</Dialog>
			{userDetails && (
				<Button
					onClick={toggleModal}
					data-cy='register-link'
					className='hover:text-brand max-w-xs m-auto hover:text-red-600 transition-colors underline-offset-4'>
					Удалить аккаунт
				</Button>
			)}
		</>
	)
}
