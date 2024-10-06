import { Box, Button, Flex, Link, Text, VStack } from "@chakra-ui/react";
import Cookies from "js-cookie";
import { useCallback } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { EAppRoutes, ECookies } from "../../configs/constants";
import Icon, { IIconName } from "../common/Icon";
import PrimaryIconButton from "../common/Buttons/PrimaryIconButton";

const Index = () => {
  const navigate = useNavigate();
  const handleLogout = async () => {
    Cookies.remove(ECookies.AUTH_TOKEN);
    navigate(EAppRoutes.LOGIN);
  };

  interface LinksProps {
    url: EAppRoutes;
    name: string;
    icon: IIconName;
  }

  const links: LinksProps[] = [
    { url: EAppRoutes.DASHBOARD, name: "My Dashboard", icon: "dashboard" },
  ];

  const renderNavbarItem = useCallback((items: LinksProps[]) => {
    return items.map((x) => (
      <SidebarItem
        key={x.url}
        href={x.url}
        title={x.name}
        size={20}
        icon={x.icon}
      />
    ));
  }, []);

  return (
    <Flex
      position="fixed"
      direction="column"
      w="297px"
      h="100vh"
      bg="white"
      pt="23px"
      pb="45px"
      px="36px"
      alignItems="start"
    >
      <Flex alignItems="center" justifyContent="space-between" w="100%">
        <Box w="60px" h="60px" borderRadius="13px" overflow="hidden">
          <NavLink to="/"></NavLink>
        </Box>
        <PrimaryIconButton aria-label="menu-button" iconName="sun" />
      </Flex>
      <Box h="60px" />
      <VStack align="start" spacing="40px">
        {renderNavbarItem(links)}
      </VStack>
      <Flex flex={1} />
      <Button
        variant="unstyled"
        color="red.500"
        _focus={{
          boxShadow: "none",
        }}
        onClick={handleLogout}
        _hover={{ color: "brand.600" }}
      >
        <Flex alignItems="center">
          <Icon icon="logout" size={20} />
          <Text
            ml="15px"
            fontWeight="semibold"
            fontSize="18px"
            lineHeight="34px"
            letterSpacing="0.72px"
          >
            Log Out
          </Text>
        </Flex>
      </Button>
    </Flex>
  );
};

export default Index;

interface SidebarItemProps {
  href: EAppRoutes;
  icon: IIconName;
  size: number;
  title: string;
}
const SidebarItem = ({ href, icon, size, title }: SidebarItemProps) => {
  return (
    <Link
      as={NavLink}
      end
      to={href}
      _hover={{ textDecoration: "none", color: "brand.500" }}
      _focus={{ boxShadow: "none" }}
      _activeLink={{ color: "brand.500" }}
    >
      <Flex alignItems="center">
        <Icon icon={icon} size={size} />

        <Text
          ml="15px"
          fontWeight="semibold"
          fontSize="18px"
          lineHeight="34px"
          letterSpacing="0.72px"
        >
          {title}
        </Text>
      </Flex>
    </Link>
  );
};
