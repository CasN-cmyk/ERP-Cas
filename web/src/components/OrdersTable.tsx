import { Badge, HStack, Table, Tbody, Td, Th, Thead, Tr } from '@chakra-ui/react';

type Order = {
  id: number;
  external_id?: string;
  status: string;
  grand_total: number;
  created_at: string;
};

const statusColor: Record<string, string> = {
  draft: 'gray',
  new: 'blue',
  paid: 'green',
  fulfilled: 'purple',
  return: 'orange',
  cancelled: 'red',
};

const OrdersTable: React.FC<{ orders: Order[] }> = ({ orders }) => {
  return (
    <Table size="sm">
      <Thead>
        <Tr>
          <Th>Order</Th>
          <Th>Status</Th>
          <Th isNumeric>Bedrag</Th>
          <Th>Datum</Th>
        </Tr>
      </Thead>
      <Tbody>
        {orders.map((order) => (
          <Tr key={order.id}>
            <Td>#{order.external_id ?? order.id}</Td>
            <Td>
              <Badge colorScheme={statusColor[order.status] ?? 'gray'} textTransform="capitalize">
                {order.status}
              </Badge>
            </Td>
            <Td isNumeric>€ {order.grand_total.toFixed(2)}</Td>
            <Td>{new Date(order.created_at).toLocaleDateString('nl-NL')}</Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  );
};

export default OrdersTable;
