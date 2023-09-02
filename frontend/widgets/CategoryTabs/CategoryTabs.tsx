'use client'
import AccessTimeIcon from '@mui/icons-material/AccessTime'
import StarIcon from '@mui/icons-material/Star'
import WhatshotIcon from '@mui/icons-material/Whatshot'
import {
	BottomNavigation,
	BottomNavigationAction,
	Box,
	Tab,
	Tabs,
} from '@mui/material'
import React, { useState } from 'react'

export const CategoryTabs = () => {
	const [value, setValue] = useState(0)

	const handleChange = (event: React.SyntheticEvent, newValue: number) => {
		setValue(newValue)
	}

	return (
		<Box sx={tabsContainer}>
			<Tabs
				sx={desktopTabs}
				orientation='vertical'
				value={value}
				onChange={handleChange}
				aria-label='icon label tabs example'>
				<Tab icon={<AccessTimeIcon />} label='ПОСЛЕДНИЕ' />
				<Tab icon={<WhatshotIcon />} label='ОТКРЫТЫЕ' />
				<Tab icon={<StarIcon />} label='ЛУЧШИЕ' />
			</Tabs>
			<BottomNavigation
				showLabels
				sx={mobileTabs}
				value={value}
				onChange={handleChange}
				aria-label='icon label tabs example'>
				<BottomNavigationAction label='Новые' icon={<AccessTimeIcon />} />
				<BottomNavigationAction label='Открытые' icon={<WhatshotIcon />} />
				<BottomNavigationAction label='Лучшие' icon={<StarIcon />} />
			</BottomNavigation>
		</Box>
	)
}

const desktopTabs = {
	display: { md: 'flex', xs: 'none' },
}
const mobileTabs = {
	display: { md: 'none', xs: 'flex' },
	width: '100%',
	justifyContent: 'center',
	alignItems: 'center',
	px: 4,
}

const tabsContainer = {
	position: { md: 'sticky', xs: 'fixed' },
	height: { md: 'auth', xs: '100px' },
	top: { md: 90, xs: 'none' },
	bottom: { md: 0, xs: -40 },
	left: { md: 0, xs: 0 },
	zIndex: 1000,
	width: { md: 'auto', xs: '100%' },
	display: { md: 'inline-block', xs: 'flex' },
	backgroundColor: { md: 'transparent', xs: '#181818' },
	justifyContent: { md: 'start', xs: 'center' },
}
