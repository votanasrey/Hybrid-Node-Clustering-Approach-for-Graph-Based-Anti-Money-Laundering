import { Flex, Text, VStack, Heading } from "@chakra-ui/react";
import React from "react";

const Dashboard: React.FC = () => {
  return (
    <>
      <Flex
        direction="column"
        w="100%"
        px={["10px", "10px", "10px", "10px", "33px", "33px"]}
        py="20px"
      >
        <Flex
          direction={["column", "column", "column", "column", "row"]}
          w="100%"
          alignItems={["start", "start", "start", "start", "center"]}
          justifyContent="space-between"
        >
          <VStack align="start">
            <Heading fontSize="48px" color="#4C4C4C" fontWeight="700">
              Dashboard
            </Heading>
            <Text fontSize="20px" color="#4C4C4C" fontWeight="400">
              Hello Admin, Welcome back!
            </Text>
          </VStack>
        </Flex>

        {/* Card */}
      </Flex>
    </>
  );
};

export default Dashboard;
