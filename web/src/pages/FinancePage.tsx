import { Box, Heading, SimpleGrid, Stat, StatHelpText, StatLabel, StatNumber, Table, Tbody, Td, Th, Thead, Tr } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import client from '../api/client';

const FinancePage = () => {
  const { data: kpis } = useQuery(['finance-kpis'], async () => (await client.get('/reports/kpis')).data);
  const { data: vat } = useQuery(['finance-vat'], async () => (await client.get('/reports/vat')).data);

  return (
    <Box>
      <Heading size="lg" mb={6}>
        Finance
      </Heading>
      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} mb={8}>
        <Stat bg="white" p={4} borderRadius="xl" boxShadow="sm">
          <StatLabel>Omzet (excl. btw)</StatLabel>
          <StatNumber>€ {(kpis?.revenue_ex ?? 0).toLocaleString('nl-NL')}</StatNumber>
          <StatHelpText>Totale omzet</StatHelpText>
        </Stat>
        <Stat bg="white" p={4} borderRadius="xl" boxShadow="sm">
          <StatLabel>BTW</StatLabel>
          <StatNumber>€ {(kpis?.vat_total ?? 0).toLocaleString('nl-NL')}</StatNumber>
          <StatHelpText>Aangifte totaal</StatHelpText>
        </Stat>
        <Stat bg="white" p={4} borderRadius="xl" boxShadow="sm">
          <StatLabel>Brutomarge</StatLabel>
          <StatNumber>€ {(kpis?.margin ?? 0).toLocaleString('nl-NL')}</StatNumber>
          <StatHelpText>{Math.round(kpis?.margin_pct ?? 0)}%</StatHelpText>
        </Stat>
      </SimpleGrid>
      <Box bg="white" p={6} borderRadius="xl" boxShadow="sm">
        <Heading size="md" mb={4}>
          BTW overzicht
        </Heading>
        <Table>
          <Thead>
            <Tr>
              <Th>Tarief</Th>
              <Th isNumeric>Bedrag</Th>
            </Tr>
          </Thead>
          <Tbody>
            {(vat ?? []).map((rate: any) => (
              <Tr key={rate.tax_rate}>
                <Td>{rate.tax_rate}%</Td>
                <Td isNumeric>€ {Number(rate.vat ?? 0).toFixed(2)}</Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    </Box>
  );
};

export default FinancePage;
