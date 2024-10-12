import { Avatar, Button, Flex, Heading, Text, VStack } from "@chakra-ui/react";
import React from "react";
import Icon from "../common/Icon";

const Topbar: React.FC = () => {
  return (
    <Flex
      px="33px"
      py="20px"
      justifyContent="space-between"
      alignItems="center"
    >
      <Heading lineHeight={"54px"} fontSize={"36px"}>
        Anomaly Detection System
      </Heading>
      <Flex gap={4}>
        <Flex
          h="52px"
          w="52px"
          bgColor="white"
          justifyContent="center"
          alignItems="center"
          borderRadius="50"
          _hover={{ cursor: "pointer" }}
        >
          <Icon icon="bell" size={20} />
        </Flex>

        <Flex
          h="52px"
          w="52px"
          bgColor="white"
          justifyContent="center"
          alignItems="center"
          borderRadius="50"
          _hover={{ cursor: "pointer" }}
        >
          <Icon icon="settings" size={20} />
        </Flex>
        <VStack>
          <Text fontWeight="semibold" fontSize="14px" letterSpacing="0.25px">
            Seanglay
          </Text>
          <Text fontWeight="regular" fontSize="14px" letterSpacing="0.25px">
            Admin
          </Text>
        </VStack>

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
    </Flex>
  );
};

export default Topbar;
