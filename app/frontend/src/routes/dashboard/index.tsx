import { Flex, Text } from "@chakra-ui/react";
import React from "react";
import Icon from "../../components/common/Icon";

const Dashboard: React.FC = () => {
  return (
    <>
      <Flex
        direction="column"
        w="100%"
        px={["10px", "10px", "10px", "10px", "33px", "33px"]}
        py="20px"
      >
        <Flex justifyContent={"space-evenly"}>
          {Array.from({ length: 5 }).map((_, index: number) => (
            <Flex gap={10} key={index}>
              <Flex
                h={"70px"}
                w={"70px"}
                bg="black"
                justifyContent="center"
                alignItems="center"
                borderRadius="50%"
              >
                <Icon icon="user" size={20} color="white" />
              </Flex>
              <Flex flexDirection={"column"} gap={2}>
                <Text fontWeight={"400"} color="lightGray" size={"18px"}>
                  Account
                </Text>
                <Text color="black" size={"36px"} fontWeight={"700"}>
                  666
                </Text>
              </Flex>
            </Flex>
          ))}
        </Flex>
      </Flex>
    </>
  );
};

export default Dashboard;
