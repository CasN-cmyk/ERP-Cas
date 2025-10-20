import { Box, Button, FormControl, FormLabel, Heading, Input, SimpleGrid, useToast } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useEffect } from 'react';
import client from '../api/client';

const schema = z.object({
  companyName: z.string().min(2),
  email: z.string().email(),
  primary: z.string().min(4),
  secondary: z.string().min(4),
});

type FormValues = z.infer<typeof schema>;

const SettingsPage = () => {
  const toast = useToast();
  const { register, handleSubmit, setValue } = useForm<FormValues>({
    resolver: zodResolver(schema),
  });

  useEffect(() => {
    const load = async () => {
      const response = await client.get('/settings/core');
      setValue('companyName', response.data.value.company.name);
      setValue('email', response.data.value.company.email);
      setValue('primary', response.data.value.brand.primary);
      setValue('secondary', response.data.value.brand.secondary);
    };
    load();
  }, [setValue]);

  const onSubmit = handleSubmit(async (values) => {
    await client.post('/settings/core', {
      brand: {
        primary: values.primary,
        secondary: values.secondary,
        logo_url: null,
      },
      company: {
        name: values.companyName,
        kvk: '12345678',
        vat_id: 'NL1234B01',
        iban: 'NL00BANK0123456789',
        email: values.email,
        phone: '+31...',
        address: {
          street: 'Laan 1',
          zip: '1234AB',
          city: 'Amsterdam',
          country: 'NL',
        },
        invoice: {
          number_pattern: 'INV-{YYYY}-{SEQ5}',
          footer: 'Bedankt voor uw bestelling!',
          default_tax_rate: 21,
        },
      },
      integrations: {
        shopify: {
          enabled: false,
          store: '',
          api_key: '',
          api_secret: '',
          access_token: '',
          webhook_secret: '',
        },
        bol: {
          enabled: false,
          client_id: '',
          client_secret: '',
          api_base: 'https://api.bol.com/retailer',
          webhook_secret: '',
        },
      },
    });
    toast({ title: 'Instellingen opgeslagen', status: 'success' });
  });

  return (
    <Box>
      <Heading size="lg" mb={6}>
        Instellingen
      </Heading>
      <Box as="form" onSubmit={onSubmit} bg="white" p={6} borderRadius="xl" boxShadow="sm">
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
          <FormControl>
            <FormLabel>Bedrijfsnaam</FormLabel>
            <Input {...register('companyName')} />
          </FormControl>
          <FormControl>
            <FormLabel>E-mail</FormLabel>
            <Input type="email" {...register('email')} />
          </FormControl>
          <FormControl>
            <FormLabel>Primaire kleur</FormLabel>
            <Input type="color" {...register('primary')} />
          </FormControl>
          <FormControl>
            <FormLabel>Secundaire kleur</FormLabel>
            <Input type="color" {...register('secondary')} />
          </FormControl>
        </SimpleGrid>
        <Button mt={8} colorScheme="blue" type="submit">
          Opslaan
        </Button>
      </Box>
    </Box>
  );
};

export default SettingsPage;
