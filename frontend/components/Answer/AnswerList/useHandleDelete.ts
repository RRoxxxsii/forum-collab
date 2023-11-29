// import { useState } from 'react'

// export const useHandleSolve = <T>(setData: <T>) => {
// 	const [newData, setNewData] = useState<T>()

// 		const handleDelete = ({
// 		id,
// 		model,
// 		setQuestionData,
// 		questionData,
// 	}: {
// 		id: number
// 		model: IModelType
// 		setQuestionData: React.Dispatch<SetStateAction<IQuestion>>
// 		questionData: IQuestion
// 	}) => {
// 		DeleteContent({
// 			id: id,
// 			model: model,
// 		})
// 		if (model === 'answer') {
// 			setQuestionData({
// 				...questionData,
// 				answers: questionData.answers.filter((answer) => answer.id !== id),
// 			})
// 		}
// 		if (model === 'comment') {
// 			//why updating nested data has to be that complicated :((((((((((((((((((((((()))))))))))))))))))))))
// 			const updatedQuestionData = {
// 				...questionData,
// 				answers: questionData.answers.map((answer) => {
// 					if (answer.comments) {
// 						return {
// 							...answer,
// 							comments: answer.comments.filter((comment) => comment.id !== id),
// 						}
// 					}
// 					return answer
// 				}),
// 			}
// 			setQuestionData(updatedQuestionData)
// 		}
// 	}
// }
