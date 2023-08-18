'use client'

import GitHubIcon from '@mui/icons-material/GitHub'
import GoogleIcon from '@mui/icons-material/Google'
import { IconButton } from '@mui/material'
import { signIn } from 'next-auth/react'

export const OauthActions = () => {
	return (
		<div className='flex justify-center'>
			<IconButton
				onClick={() => signIn('google', { callbackUrl: '/' })}
				aria-label='delete'>
				<GoogleIcon />
			</IconButton>
			<IconButton
				onClick={() => signIn('github', { callbackUrl: '/' })}
				aria-label='delete'>
				<GitHubIcon />
			</IconButton>
		</div>
	)
}
