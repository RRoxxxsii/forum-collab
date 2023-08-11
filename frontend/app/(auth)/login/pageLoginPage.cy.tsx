import LoginPage from './page'

describe('<LoginPage />', () => {
	it('renders', () => {
		// see: https://on.cypress.io/mounting-react
		cy.mount(<LoginPage />)
	})
	it('leads to register', () => {
		// see: https://on.cypress.io/mounting-react
		cy.mount(<LoginPage />)
		cy.get('[data-cy=register-link]').click()

		cy.intercept('GET', 'http://localhost:8080/register', {
			statusCode: 404,
			body: 'Not Found',
		}).as('registerRequest')
	})
})
