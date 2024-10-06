import { extendTheme } from "@chakra-ui/react";
import { createBreakpoints } from "@chakra-ui/theme-tools";

const breakpoints = createBreakpoints({
  sm: "40em",
  md: "52em",
  lg: "64em",
  xl: "80em",
});

const theme = extendTheme({
  colors: {
    black: "#16161D",
    gray: {
      50: "#FAFAFA",
      100: "#F1F2F6",
      200: "#E2E5F1",
      300: "#CFD6EB",
      400: "#ABB2C6",
      500: "#8B91A5",
      600: "#63697C",
      700: "#505668",
      800: "#313849",
      900: "#111827",
    },
    brand: {
      500: "#123962",
      600: "#2754ba",
      700: "#00aee6",
      800: "#799eb2",
      900: "#b1d4e5",
    },
  },
  breakpoints,
});

export { theme };
