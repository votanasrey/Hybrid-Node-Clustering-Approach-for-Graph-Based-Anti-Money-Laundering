import { Flex } from "@chakra-ui/react";
import React from "react";
import Sidebar from "../Sidebar";
import Topbar from "../Topbar";

interface LayoutProps {
  children: React.ReactNode;
}

const index: React.FC<LayoutProps> = ({ children }) => {
  return (
    <Flex>
      <Sidebar />
      <Flex
        maxW="full"
        pl="297px"
        bg="#F7F7FC"
        minH="100vh"
        direction="column"
        flex={1}
      >
        <Topbar />
        <Flex flex={1} flexShrink={0}>
          {children}
        </Flex>
      </Flex>
    </Flex>
  );
};

export default index;
