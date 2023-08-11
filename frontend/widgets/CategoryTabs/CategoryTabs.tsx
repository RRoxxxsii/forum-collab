'use client'
import AccessTimeIcon from '@mui/icons-material/AccessTime'
import StarIcon from '@mui/icons-material/Star'
import WhatshotIcon from '@mui/icons-material/Whatshot'
import { Box, Tab, Tabs } from '@mui/material'
import React, { useState } from 'react'

export const CategoryTabs = () => {
	const [value, setValue] = useState(0)

	const handleChange = (event: React.SyntheticEvent, newValue: number) => {
		setValue(newValue)
	}

	return (
		<Box className='w-32 h-screen'>
			<Box className='flex flex-col justify-between items-center fixed'>
				<Tabs
					orientation='vertical'
					value={value}
					onChange={handleChange}
					aria-label='icon label tabs example'>
					<Tab icon={<AccessTimeIcon />} label='ПОСЛЕДНИЕ' />
					<Tab icon={<WhatshotIcon />} label='ОТКРЫТЫЕ' />
					<Tab icon={<StarIcon />} label='ЛУЧШИЕ' />
				</Tabs>
			</Box>
		</Box>
	)
}
