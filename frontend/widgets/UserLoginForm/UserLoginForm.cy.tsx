import { UserLoginForm } from './UserLoginForm'

describe('<UserLoginForm />', () => {
	it('renders', () => {
		// see: https://on.cypress.io/mounting-react
		cy.mount(<UserLoginForm />)
	})
	it('should successfully submit the form with valid data', () => {
		// Fill in the email and password fields
		cy.mount(<UserLoginForm />)

		cy.get('[data-cy=email]').type('test123@gmail.com')
		cy.get('[data-cy=password]').type('test123')

		// Submit the form
		cy.get('[data-cy=submit-button]').click()

		// Assert that the form submission was successful (you can adjust this assertion based on your actual behavior)
	})

	it('should display errors for empty fields', () => {
		cy.mount(<UserLoginForm />)

		// Submit the form without filling in any fields
		cy.get('[data-cy=submit-button]').click()

		// Assert that error messages are displayed for both email and password fields
		cy.contains('Неправильный формат почтового адреса')
		cy.contains('Пароль должен содержать минимум 6 символов')
	})

	it('should display error for invalid email', () => {
		cy.mount(<UserLoginForm />)
		// Fill in an invalid email format
		cy.get('[data-cy=email]').type('invalid-email')

		// Submit the form
		cy.get('[data-cy=submit-button]').click()

		// Assert that error message is displayed for email field
		cy.contains('Неправильный формат почтового адреса')
	})

	it('should display error for incorrect password', () => {
		cy.mount(<UserLoginForm />)
		// Fill in the email and an incorrect password
		cy.get('[data-cy=email]').type('test@example.com')
		cy.get('[data-cy=password]').type('123')

		// Submit the form
		cy.get('[data-cy=submit-button]').click()

		// Assert that error message is displayed for password field
		cy.contains('Пароль должен содержать минимум 6 символов')
	})
})
