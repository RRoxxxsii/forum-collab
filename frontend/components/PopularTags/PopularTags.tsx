'use client'
import { Tag } from '@/shared/Tag'
import { BASE_URL } from '@/shared/constants'
import { ITag } from '@/types'
import { useEffect, useState } from 'react'
import 'swiper/css'
import { Swiper, SwiperSlide } from 'swiper/react'

export const PopularTags = () => {
	const [popularTags, setPopularTags] = useState<ITag[]>([])

	const fetchPopularTags = async () => {
		try {
			const response = await fetch(BASE_URL + '/forum/top-tags/')

			const result = await response.json()
			if (!response.ok) {
				throw new Error(response.statusText ?? result)
			}
			setPopularTags(result)
		} catch (error) {}
	}

	useEffect(() => {
		fetchPopularTags()
	}, [])

	return (
		<Swiper spaceBetween={20} slidesPerView={13}>
			{popularTags.map((tag) => (
				<SwiperSlide>
					<Tag tagData={tag} />
				</SwiperSlide>
			))}
		</Swiper>
	)
}
