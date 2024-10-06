import {
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  InputProps,
  Spacer,
} from "@chakra-ui/react";
import { FormikErrors } from "formik";
import React from "react";

interface TextInputProps extends InputProps {
  error?:
    | string
    | string[]
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    | FormikErrors<any>
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    | FormikErrors<any>[]
    | undefined;
  label?: string;
}

const TextInput: React.FC<TextInputProps> = ({ error, label, ...rest }) => {
  return (
    <>
      <FormControl isInvalid={!!error} mb="5px">
        <FormLabel htmlFor={rest.name}>{label}</FormLabel>
        <Input
          borderRadius="16px"
          px="24px"
          py="14px"
          h="64px"
          w="100%"
          color="gray.900"
          fontSize="15px"
          lineHeight="24px"
          letterSpacing="0.75px"
          borderColor={error ? "red.500" : "gray.200"}
          bg={error ? "red.50" : "white"}
          type="text"
          _focus={{ boxShadow: "0 0 0 1px #FFBE00", borderColor: "brand.500" }}
          {...rest}
        />
        {!!error && <FormErrorMessage>error</FormErrorMessage>}
        <Spacer h="30px" />
      </FormControl>
    </>
  );
};

export default TextInput;
