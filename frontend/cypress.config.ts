import { defineConfig } from 'cypress'

export default defineConfig({
	component: {
		devServer: {
			framework: 'next',
			bundler: 'webpack',
		},
	},

	e2e: {
		specPattern: '**/*.cy.{js,jsx,ts,tsx}',
		setupNodeEvents(on, config) {},
	},
})
