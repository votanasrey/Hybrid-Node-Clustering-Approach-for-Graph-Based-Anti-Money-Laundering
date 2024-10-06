import { Avatar, Box, Button, Flex, Text } from "@chakra-ui/react";
import React from "react";

const Topbar: React.FC = () => {
  return (
    <Flex px="33px" py="20px" justifyContent="flex-end" alignItems="center">
      <Text fontWeight="semibold" fontSize="14px" letterSpacing="0.25px">
        Admin
      </Text>
      <Box w="10px" />
      <Button
        bg="red"
        borderColor="white"
        borderWidth="2px"
        p="0px"
        w="52px"
        h="52px"
        borderRadius="52px"
        _hover={{ borderColor: "brand.500" }}
      >
        <Avatar
          w="48px"
          h="48px"
          src="https://i.seadn.io/gae/Eu9zj3y2IrCu6QsPRUoQJiLRXt7dahdlYz414oj4LEwCYdiIOD0RS4WFsnu2Ur0QOBAZe6TRH0SeMhM_OZ2mcToScp_yTjdtSS0-dw?auto=format&w=1000"
        />
      </Button>
    </Flex>
  );
};

export default Topbar;
