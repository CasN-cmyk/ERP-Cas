import { Box, Heading, Table, Tbody, Td, Th, Thead, Tr } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import client from '../api/client';

const CustomersPage = () => {
  const { data: customers } = useQuery(['customers'], async () => {
    const response = await client.get('/customers');
    return response.data;
  });

  return (
    <Box>
      <Heading size="lg" mb={6}>
        Klanten
      </Heading>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Naam</Th>
            <Th>Email</Th>
            <Th>Telefoon</Th>
            <Th>Aantal adressen</Th>
          </Tr>
        </Thead>
        <Tbody>
          {(customers ?? []).map((customer: any) => (
            <Tr key={customer.id}>
              <Td>{customer.name}</Td>
              <Td>{customer.email}</Td>
              <Td>{customer.phone}</Td>
              <Td>{customer.addresses?.length ?? 0}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default CustomersPage;
