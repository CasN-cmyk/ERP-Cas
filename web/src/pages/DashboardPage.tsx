import { Box, Grid, GridItem, Heading, SimpleGrid, Stat, StatHelpText, StatLabel, StatNumber } from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import { useMemo } from 'react';
import client from '../api/client';
import RevenueChart from '../components/RevenueChart';
import OrdersTable from '../components/OrdersTable';

const DashboardPage = () => {
  const { data: kpis } = useQuery(['kpis'], async () => {
    const response = await client.get('/reports/kpis');
    return response.data;
  });

  const { data: sales } = useQuery(['sales'], async () => {
    const response = await client.get('/reports/sales', { params: { group_by: 'month' } });
    return response.data;
  });

  const { data: orders } = useQuery(['orders', 'latest'], async () => {
    const response = await client.get('/orders', { params: { limit: 5 } });
    return response.data;
  });

  const stats = useMemo(
    () => [
      { label: 'Omzet', value: kpis?.revenue_ex ?? 0, helpText: 'Exclusief BTW' },
      { label: 'Brutomarge', value: kpis?.margin ?? 0, helpText: `${Math.round(kpis?.margin_pct ?? 0)}%` },
      { label: 'Voorraadwaarde', value: kpis?.inventory_value ?? 0, helpText: 'Totaal op voorraad' },
      { label: 'Openstaande betalingen', value: kpis?.open_payments ?? 0, helpText: 'Nog te innen' },
    ],
    [kpis]
  );

  return (
    <Grid templateColumns={{ base: '1fr', xl: '2fr 1fr' }} gap={8} alignItems="start">
      <GridItem>
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} mb={8}>
          {stats.map((stat) => (
            <Stat key={stat.label} p={4} bg="white" borderRadius="xl" boxShadow="sm">
              <StatLabel>{stat.label}</StatLabel>
              <StatNumber>€ {stat.value.toLocaleString('nl-NL', { maximumFractionDigits: 0 })}</StatNumber>
              <StatHelpText>{stat.helpText}</StatHelpText>
            </Stat>
          ))}
        </SimpleGrid>
        <Box bg="white" borderRadius="xl" boxShadow="sm" p={6} mb={8}>
          <Heading size="md" mb={4}>
            Omzet & Marge
          </Heading>
          <RevenueChart data={sales ?? []} />
        </Box>
      </GridItem>
      <GridItem>
        <Box bg="white" borderRadius="xl" boxShadow="sm" p={6}>
          <Heading size="md" mb={4}>
            Laatste orders
          </Heading>
          <OrdersTable orders={orders ?? []} />
        </Box>
      </GridItem>
    </Grid>
  );
};

export default DashboardPage;
