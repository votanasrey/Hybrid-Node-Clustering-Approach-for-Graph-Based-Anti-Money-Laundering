import { createStandaloneToast } from "@chakra-ui/toast";

const { toast } = createStandaloneToast();

export const pushNotification = (msg: string, isSuccess = true) => {
  return toast({
    title: isSuccess ? "SUCCESS" : "ERROR",
    description: msg,
    status: isSuccess ? "success" : "error",
    duration: 9000,
    isClosable: true,
  });
};
