import { extendTheme, ThemeConfig } from '@chakra-ui/react';

const config: ThemeConfig = {
  initialColorMode: 'light',
  useSystemColorMode: false,
};

const theme = extendTheme({
  config,
  styles: {
    global: {
      body: {
        bg: 'gray.50',
      },
    },
  },
  colors: {
    brand: {
      50: '#e9f2ff',
      100: '#c0d4ff',
      200: '#97b7ff',
      300: '#6d9aff',
      400: '#447dff',
      500: '#2563eb',
      600: '#1b4db8',
      700: '#123785',
      800: '#092152',
      900: '#010b22',
    },
  },
});

export default theme;
export type AppTheme = typeof theme;
