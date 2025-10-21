module.exports = {
  testEnvironment: 'jsdom',
  collectCoverageFrom: [
    'js/**/*.js',
    'src/**/*.js',
    '!js/**/*.test.js',
    '!src/**/*.test.js',
  ],
  testMatch: [
    '**/__tests__/**/*.js',
    '**/*.test.js',
  ],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@js/(.*)$': '<rootDir>/js/$1',
    '^@assets/(.*)$': '<rootDir>/assets/$1',
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  transform: {
    '^.+\\.js$': 'babel-jest',
  },
};
