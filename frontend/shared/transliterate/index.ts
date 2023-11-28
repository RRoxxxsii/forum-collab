const converter: { [key: string]: string } = {
	Ё: 'E',
	Й: 'I',
	Ц: 'С',
	У: 'U',
	К: 'K',
	Е: 'E',
	Н: 'N',
	Г: 'G',
	Ш: 'Sh',
	Щ: 'Sh',
	З: 'Z',
	Х: 'H',
	Ъ: '',
	ё: 'yo',
	й: 'i',
	ц: 'ts',
	у: 'u',
	к: 'k',
	е: 'e',
	н: 'n',
	г: 'g',
	ш: 'sh',
	щ: 'sh',
	з: 'z',
	х: 'h',
	ъ: '',
	Ф: 'F',
	Ы: 'I',
	В: 'V',
	А: 'A',
	П: 'P',
	Р: 'R',
	О: 'O',
	Л: 'L',
	Д: 'D',
	Ж: 'Zh',
	Э: 'E',
	ф: 'f',
	ы: 'i',
	в: 'v',
	а: 'a',
	п: 'p',
	р: 'r',
	о: 'o',
	л: 'l',
	д: 'd',
	ж: 'zh',
	э: 'e',
	Я: 'Ya',
	Ч: 'Ch',
	С: 'S',
	М: 'M',
	И: 'I',
	Т: 'T',
	Ь: '',
	Б: 'B',
	Ю: 'Yu',
	я: 'ya',
	ч: 'ch',
	с: 's',
	м: 'm',
	и: 'i',
	т: 't',
	ь: '',
	б: 'b',
	ю: 'yu',
}

export function Transliterate(word: string): string {
	return word
		.split('')
		.map(function (char) {
			if (converter[char] !== undefined) {
				return converter[char]
			} else if (char === 'ь' || char === 'ъ') {
				return ''
			} else {
				return char
			}
		})
		.join('')
		.replaceAll(/ /g, '_')
}
