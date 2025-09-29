import ts from '@typescript-eslint/eslint-plugin';
import vue from 'eslint-plugin-vue';
import prettier from 'eslint-plugin-prettier';

/** @type {import('eslint').Linter.Config[]} */
export default [
  {
    files: ['**/*.{ts,tsx,vue,js}'],

    languageOptions: {
      parser: '@typescript-eslint/parser',
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
    },

    plugins: { '@typescript-eslint': ts, vue, prettier },

    rules: {
      'prettier/prettier': 'error',
      indent: ['error', 2],
      '@typescript-eslint/no-unused-vars': 'error',
    },
  },
];
