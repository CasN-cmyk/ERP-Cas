import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import axios from 'axios';

export type BrandSettings = {
  primary: string;
  secondary: string;
  logo_url?: string | null;
};

export type SettingsState = {
  brand: BrandSettings;
};

const defaultSettings: SettingsState = {
  brand: {
    primary: '#2563eb',
    secondary: '#1e293b',
    logo_url: null,
  },
};

const SettingsContext = createContext<SettingsState>(defaultSettings);

export const SettingsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [settings, setSettings] = useState<SettingsState>(defaultSettings);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const response = await axios.get(`${__API_BASE__}/settings/core`);
        setSettings({
          brand: response.data.value.brand,
        });
      } catch (error) {
        console.warn('Failed to load settings', error);
      }
    };
    fetchSettings();
  }, []);

  const value = useMemo(() => settings, [settings]);

  return <SettingsContext.Provider value={value}>{children}</SettingsContext.Provider>;
};

export const useSettings = () => useContext(SettingsContext);
