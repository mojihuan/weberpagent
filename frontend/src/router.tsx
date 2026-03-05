import { createBrowserRouter } from 'react-router-dom';
import { MainLayout } from './components/layout';
import { DashboardPage, AIGeneratePage, VisualTestPage, TestCasesPage } from './pages';

// Placeholder pages for routes not yet implemented
function PlaceholderPage({ title }: { title: string }) {
  return (
    <div className="flex items-center justify-center h-[60vh]">
      <div className="text-center">
        <h1 className="text-2xl font-semibold text-foreground mb-2">{title}</h1>
        <p className="text-foreground-secondary">页面开发中...</p>
      </div>
    </div>
  );
}

export const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: 'test-cases',
        element: <TestCasesPage />,
      },
      {
        path: 'ai-generate',
        element: <AIGeneratePage />,
      },
      {
        path: 'test-execution',
        element: <PlaceholderPage title="测试执行中心" />,
      },
      {
        path: 'visual-test',
        element: <VisualTestPage />,
      },
      {
        path: 'reports',
        element: <PlaceholderPage title="测试报告" />,
      },
      {
        path: 'self-healing',
        element: <PlaceholderPage title="自愈记录" />,
      },
    ],
  },
]);