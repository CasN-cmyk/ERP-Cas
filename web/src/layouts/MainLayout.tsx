import { Box, Flex, HStack, Icon, Link, Text, VStack } from '@chakra-ui/react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { FiBarChart2, FiBox, FiHome, FiSettings, FiShoppingCart, FiUsers } from 'react-icons/fi';
import { MdOutlineHandshake } from 'react-icons/md';
import { useSettings } from '../context/SettingsContext';

const navItems = [
  { label: 'Dashboard', href: '/', icon: FiHome },
  { label: 'Products', href: '/products', icon: FiBox },
  { label: 'Orders', href: '/orders', icon: FiShoppingCart },
  { label: 'Customers', href: '/customers', icon: FiUsers },
  { label: 'Finance', href: '/finance', icon: FiBarChart2 },
  { label: 'CRM', href: '/crm', icon: MdOutlineHandshake },
  { label: 'Settings', href: '/settings', icon: FiSettings },
];

const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  const { brand } = useSettings();

  return (
    <Flex minH="100vh">
      <Box w="240px" bg={brand.secondary} color="white" p={6} display={{ base: 'none', md: 'block' }}>
        <VStack align="flex-start" spacing={6}>
          <Text fontSize="xl" fontWeight="bold">
            Cas Commerce
          </Text>
          <VStack align="stretch" spacing={2} w="full">
            {navItems.map((item) => (
              <Link
                key={item.href}
                as={RouterLink}
                to={item.href}
                display="flex"
                alignItems="center"
                px={3}
                py={2}
                borderRadius="md"
                bg={location.pathname === item.href ? 'whiteAlpha.200' : 'transparent'}
                _hover={{ textDecoration: 'none', bg: 'whiteAlpha.300' }}
              >
                <HStack spacing={3}>
                  <Icon as={item.icon} />
                  <Text>{item.label}</Text>
                </HStack>
              </Link>
            ))}
          </VStack>
        </VStack>
      </Box>
      <Flex direction="column" flex="1" bg="gray.50">
        <Box bg="white" borderBottomWidth="1px" px={8} py={4}>
          <Text fontWeight="semibold" color={brand.secondary}>
            Welkom terug!
          </Text>
        </Box>
        <Box flex="1" p={8}>{children}</Box>
      </Flex>
    </Flex>
  );
};

export default MainLayout;
