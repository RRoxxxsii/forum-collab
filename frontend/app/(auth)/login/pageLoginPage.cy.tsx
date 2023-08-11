import LoginPage from './page'

describe('<LoginPage />', () => {
	it('renders', () => {
		// see: https://on.cypress.io/mounting-react
		cy.mount(<LoginPage />)
	})
})
