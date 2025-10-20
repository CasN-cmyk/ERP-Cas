import { Badge, Box, Heading, Table, Tbody, Td, Th, Thead, Tr } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import client from '../api/client';

const OrdersPage = () => {
  const { data: orders } = useQuery(['orders'], async () => {
    const response = await client.get('/orders');
    return response.data;
  });

  return (
    <Box>
      <Heading size="lg" mb={6}>
        Orders
      </Heading>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>#</Th>
            <Th>Klant</Th>
            <Th>Status</Th>
            <Th isNumeric>Bedrag</Th>
          </Tr>
        </Thead>
        <Tbody>
          {(orders ?? []).map((order: any) => (
            <Tr key={order.id}>
              <Td>{order.external_id ?? order.id}</Td>
              <Td>{order.customer?.name ?? 'Onbekend'}</Td>
              <Td>
                <Badge textTransform="capitalize" colorScheme={order.status === 'paid' ? 'green' : 'blue'}>
                  {order.status}
                </Badge>
              </Td>
              <Td isNumeric>€ {Number(order.grand_total ?? 0).toFixed(2)}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default OrdersPage;
