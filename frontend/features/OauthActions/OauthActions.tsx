'use client'

import GitHubIcon from '@mui/icons-material/GitHub'
import GoogleIcon from '@mui/icons-material/Google'
import { IconButton } from '@mui/material'

export const OauthActions = () => {
	return (
		<div className='flex justify-center'>
			<IconButton aria-label='delete'>
				<GoogleIcon />
			</IconButton>
			<IconButton aria-label='delete'>
				<GitHubIcon />
			</IconButton>
		</div>
	)
}
