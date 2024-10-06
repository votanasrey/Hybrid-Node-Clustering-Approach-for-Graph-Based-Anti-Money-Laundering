/* eslint-disable @typescript-eslint/no-explicit-any */
import {
  Box,
  Flex,
  Heading,
  HStack,
  Switch,
  Text,
  VStack,
} from "@chakra-ui/react";
import React, { useCallback, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Formik, Field, Form } from "formik";
import Cookies from "js-cookie";
import PrimaryButton from "../../components/common/Buttons/PrimaryButton";
import TextInput from "../../components/common/Input/TextInput";
import { formValidation } from "../../configs/formValidationSchema";
import { EAppRoutes, ECookies } from "../../configs/constants";
import { ISignInParams } from "../../state/api/auth/types";
import { apis } from "../../state/api";
import { pushNotification } from "../../utils/pushNotification";
import { useMutation } from "react-query";

const Login: React.FC = () => {
  const navigate = useNavigate();
  const { state }: any = useLocation();

  const [initialFormState] = useState<ISignInParams>({
    email: "seanglay@gmail.com",
    password: "123456",
  });

  const signInMutation = useMutation(apis.auth.signIn);
  const handleSumbit = useCallback(
    (values: ISignInParams, actions: any) => {
      signInMutation.mutate(values, {
        onSuccess: (data) => {
          Cookies.set(ECookies.AUTH_TOKEN, data.data.token);
          pushNotification("You can access your dashboard now!");
          navigate(state?.path || EAppRoutes.DASHBOARD);
        },
        onError: (error: any) => {
          const message = error?.response?.data?.message || error?.message;
          console.log(message);

          pushNotification(message, false);
        },
      });
      actions.setSubmitting(false);
    },
    [signInMutation]
  );

  return (
    <HStack>
      <Flex flex={1} bg="brand.500" h="100vh">
        <Box position="absolute" bottom="10px" left="10px">
          <Text
            color="white"
            fontSize="18px"
            lineHeight="32px"
            letterSpacing="0.75px"
          >
            v1.0.0
          </Text>
        </Box>
      </Flex>
      <Flex flex={1} alignItems="center" justifyContent="center">
        <Formik
          initialValues={initialFormState}
          validationSchema={formValidation.loginValidationSchema}
          onSubmit={handleSumbit}
        >
          {({ handleChange, values }) => (
            <VStack
              as={Form}
              spacing="22px"
              align="start"
              w={["400px", "460px"]}
              px="30px"
              mx="auto"
            >
              <Heading color="gray.900">Log In</Heading>
              <Field name="email">
                {({ field, form }: any) => (
                  <TextInput
                    {...field}
                    id="email"
                    placeholder="Username"
                    error={form.errors.email}
                    value={values.email}
                    onChange={handleChange}
                  />
                )}
              </Field>
              <Field name="password">
                {({ field, form }: any) => (
                  <TextInput
                    {...field}
                    id="password"
                    placeholder="Password"
                    error={form.errors.password}
                    value={values.password}
                    type="password"
                    onChange={handleChange}
                  />
                )}
              </Field>
              <Flex w="100%" alignItems="center" justifyContent="space-between">
                <Text
                  color="gray.900"
                  fontSize="18px"
                  lineHeight="32px"
                  letterSpacing="0.75px"
                >
                  Remember Me?
                </Text>
                <Switch pt="5px" colorScheme="brand" size="lg" />
              </Flex>
              <PrimaryButton
                isLoading={signInMutation.isLoading}
                type="submit"
                title="Log In"
              />
            </VStack>
          )}
        </Formik>
      </Flex>
    </HStack>
  );
};

export default Login;
