import { IconButton, IconButtonProps } from "@chakra-ui/react";
import React from "react";
import Icon, { IIconName } from "../../Icon";

interface PrimaryIconButtonProps extends IconButtonProps {
  iconName: IIconName;
  iconSize?: number;
}

const PrimaryIconButton: React.FC<PrimaryIconButtonProps> = ({
  iconName,
  iconSize = 24,
  ...rest
}) => {
  return (
    <IconButton
      bg="transparent"
      _hover={{ bg: "brand.900", color: "gray.900" }}
      _focus={{
        bg: "brand.900",
        color: "gray.900",
        boxShadow: "0 0 0 1px #FFBE00",
        borderColor: "brand.500",
      }}
      _active={{ bg: "brand.800", color: "gray.900" }}
      h="44px"
      ß
      w="44px"
      icon={<Icon icon={iconName} size={iconSize} />}
      {...rest}
    />
  );
};

export default PrimaryIconButton;
