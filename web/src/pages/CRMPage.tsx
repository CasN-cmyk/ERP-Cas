import { Box, Heading, SimpleGrid, Stat, StatHelpText, StatLabel, StatNumber, Table, Tbody, Td, Th, Thead, Tr } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import client from '../api/client';

const CRMPage = () => {
  const { data: leads } = useQuery(['crm', 'leads'], async () => (await client.get('/crm/leads')).data);
  const { data: deals } = useQuery(['crm', 'deals'], async () => (await client.get('/crm/deals')).data);

  return (
    <Box>
      <Heading size="lg" mb={6}>
        CRM
      </Heading>
      <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} mb={8}>
        <Stat bg="white" p={4} borderRadius="xl" boxShadow="sm">
          <StatLabel>Actieve leads</StatLabel>
          <StatNumber>{(leads ?? []).length}</StatNumber>
          <StatHelpText>Nieuwe kansen</StatHelpText>
        </Stat>
        <Stat bg="white" p={4} borderRadius="xl" boxShadow="sm">
          <StatLabel>Deals pipeline</StatLabel>
          <StatNumber>{(deals ?? []).length}</StatNumber>
          <StatHelpText>Totaal in behandeling</StatHelpText>
        </Stat>
      </SimpleGrid>
      <Box bg="white" p={6} borderRadius="xl" boxShadow="sm" mb={8}>
        <Heading size="md" mb={4}>
          Leads
        </Heading>
        <Table>
          <Thead>
            <Tr>
              <Th>Naam</Th>
              <Th>Status</Th>
              <Th>Eigenaar</Th>
            </Tr>
          </Thead>
          <Tbody>
            {(leads ?? []).map((lead: any) => (
              <Tr key={lead.id}>
                <Td>{lead.name}</Td>
                <Td>{lead.status}</Td>
                <Td>{lead.owner_id ?? '-'}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
      <Box bg="white" p={6} borderRadius="xl" boxShadow="sm">
        <Heading size="md" mb={4}>
          Deals
        </Heading>
        <Table>
          <Thead>
            <Tr>
              <Th>Titel</Th>
              <Th>Waarde</Th>
              <Th>Stage</Th>
            </Tr>
          </Thead>
          <Tbody>
            {(deals ?? []).map((deal: any) => (
              <Tr key={deal.id}>
                <Td>{deal.title}</Td>
                <Td>€ {Number(deal.value_ex ?? 0).toFixed(0)}</Td>
                <Td>{deal.stage}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    </Box>
  );
};

export default CRMPage;
