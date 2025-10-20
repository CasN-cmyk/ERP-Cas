import { Route, Routes } from 'react-router-dom';
import DashboardPage from '../pages/DashboardPage';
import ProductsPage from '../pages/ProductsPage';
import OrdersPage from '../pages/OrdersPage';
import CustomersPage from '../pages/CustomersPage';
import FinancePage from '../pages/FinancePage';
import CRMPage from '../pages/CRMPage';
import SettingsPage from '../pages/SettingsPage';
import MainLayout from '../layouts/MainLayout';

const App = () => {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/orders" element={<OrdersPage />} />
        <Route path="/customers" element={<CustomersPage />} />
        <Route path="/finance" element={<FinancePage />} />
        <Route path="/crm" element={<CRMPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </MainLayout>
  );
};

export default App;
