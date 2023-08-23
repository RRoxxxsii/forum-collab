describe('authform links', () => {
	it('leads to register route', () => {
		cy.visit('http://localhost:3000/auth/login')
		cy.get('[data-cy=register-link]').click()
		cy.wait(10000)
		cy.location('pathname').should('eq', '/auth/register')
	})
	it('leads to back to homepage', () => {
		cy.visit('http://localhost:3000/auth/login')
		cy.get('[data-cy=home-link]').click()
		cy.wait(10000)
		cy.location('pathname').should('eq', '/')
	})
})
