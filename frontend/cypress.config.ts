import { defineConfig } from 'cypress'

export default defineConfig({
	component: {
		devServer: {
			framework: 'next',
			bundler: 'webpack',
		},
	},

	e2e: {
		specPattern: '**/*.cy.ts',
		setupNodeEvents(on, config) {},
	},
})
