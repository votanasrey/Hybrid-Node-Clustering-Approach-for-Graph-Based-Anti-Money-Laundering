import { Button, ButtonProps, Text } from "@chakra-ui/react";
import React from "react";

interface PrimaryButtonProps extends ButtonProps {
  title: string;
}
const PrimaryButton: React.FC<PrimaryButtonProps> = ({ title, ...rest }) => {
  return (
    <Button
      w="100%"
      colorScheme="brand"
      variant="solid"
      h="64px"
      px="24px"
      borderRadius="16px"
      _focus={{ boxShadow: "0 0 0 1px #FFBE00", borderColor: "brand.500" }}
      {...rest}
    >
      <Text
        fontWeight="semibold"
        fontSize="18px"
        lineHeight="32px"
        textAlign="center"
        letterSpacing="0.72px"
      >
        {title}
      </Text>
    </Button>
  );
};

export default PrimaryButton;
