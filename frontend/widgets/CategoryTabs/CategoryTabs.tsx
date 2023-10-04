'use client'
import { CategoryContext, CategoryType } from '@/providers/CategoryProvider'
import { Verified } from '@mui/icons-material'
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
import { useContext } from 'react'

export const CategoryTabs = () => {
	const { category, setCategory } = useContext(CategoryContext)

	const handleCategoryChange = (
		event: React.ChangeEvent<{}>,
		newCategory: CategoryType
	) => {
		setCategory(newCategory)
	}

	return (
		<Box sx={tabsContainer}>
			<Tabs
				sx={desktopTabs}
				orientation='vertical'
				value={category}
				onChange={handleCategoryChange}
				aria-label='icon label tabs example'>
				<Tab value={'opened'} icon={<AccessTimeIcon />} label='ОТКРЫТЫЕ' />
				<Tab value={'closed'} icon={<Verified />} label='ЗАКРЫТЫЕ' />
				<Tab value={'best'} icon={<WhatshotIcon />} label='ПОПУЛЯРНЫЕ' />
			</Tabs>
			<BottomNavigation
				showLabels
				sx={mobileTabs}
				value={category}
				onChange={handleCategoryChange}
				aria-label='icon label tabs example'>
				<BottomNavigationAction
					value={'opened'}
					label='Открытые'
					icon={<AccessTimeIcon />}
				/>
				<BottomNavigationAction
					value={'closed'}
					label='Закрытые'
					icon={<Verified />}
				/>
				<BottomNavigationAction
					value={'best'}
					label='Популярные'
					icon={<WhatshotIcon />}
				/>
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
