module.exports = {
  testEnvironment: 'node',
  transform: {
    '^.+\\.ts$': 'ts-jest',
  },
  testRegex: '(/__tests__/.*|(\\.|/)(test|spec))\\.ts$',
  moduleFileExtensions: ['ts', 'js', 'json', 'node'],
  coverageDirectory: 'coverage',
  collectCoverageFrom: ['src/**/*.{ts,js}', '!src/**/*.d.ts'],
};