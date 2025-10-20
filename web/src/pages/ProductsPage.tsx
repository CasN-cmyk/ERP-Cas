import { Badge, Box, Button, Flex, Heading, HStack, Table, Tbody, Td, Th, Thead, Tr } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import client from '../api/client';

const ProductsPage = () => {
  const { data: products } = useQuery(['products'], async () => {
    const response = await client.get('/products');
    return response.data;
  });

  return (
    <Box>
      <Flex justify="space-between" align="center" mb={6}>
        <Heading size="lg">Producten</Heading>
        <Button colorScheme="blue">Nieuw product</Button>
      </Flex>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>SKU</Th>
            <Th>Naam</Th>
            <Th>Voorraad</Th>
            <Th>Kostprijs</Th>
            <Th>Status</Th>
          </Tr>
        </Thead>
        <Tbody>
          {(products ?? []).map((product: any) => (
            <Tr key={product.id}>
              <Td>{product.sku}</Td>
              <Td>{product.name}</Td>
              <Td>{product.inventory_cache?.available ?? 0}</Td>
              <Td>€ {Number(product.cost_price ?? 0).toFixed(2)}</Td>
              <Td>
                <Badge colorScheme={product.status === 'active' ? 'green' : 'gray'} textTransform="capitalize">
                  {product.status}
                </Badge>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default ProductsPage;
