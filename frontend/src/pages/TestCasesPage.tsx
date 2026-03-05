import { Header } from '../components/layout';
import { Plus, MoreHorizontal } from 'lucide-react';
import { Button } from '../components/ui';

type TestStatus = 'passed' | 'failed' | 'running';

interface TestCase {
  id: number;
  name: string;
  module: string;
  status: TestStatus;
  lastRun: string;
}

const testCases: TestCase[] = [
  { id: 1, name: '用户登录流程测试', module: '用户模块', status: 'passed', lastRun: '2024-03-05' },
  { id: 2, name: '商品搜索功能测试', module: '商品模块', status: 'passed', lastRun: '2024-03-05' },
  { id: 3, name: '订单支付流程测试', module: '订单模块', status: 'failed', lastRun: '2024-03-04' },
  { id: 4, name: '用户注册验证测试', module: '用户模块', status: 'running', lastRun: '2024-03-05' },
  { id: 5, name: '商品详情展示测试', module: '商品模块', status: 'passed', lastRun: '2024-03-03' },
  { id: 6, name: '购物车功能测试', module: '订单模块', status: 'passed', lastRun: '2024-03-04' },
];

const statusStyles: Record<TestStatus, string> = {
  passed: 'bg-success/10 text-success',
  failed: 'bg-danger/10 text-danger',
  running: 'bg-warning/10 text-warning',
};

const statusLabels: Record<TestStatus, string> = {
  passed: '通过',
  failed: '失败',
  running: '执行中',
};

export function TestCasesPage() {
  return (
    <div className="space-y-6">
      <Header
        title="测试用例管理"
        subtitle="管理和维护所有测试用例"
        action={
          <Button icon={<Plus className="w-4 h-4" />}>新建用例</Button>
        }
      />

      {/* Filters */}
      <div className="flex items-center gap-4">
        <select className="px-3 py-2 bg-background-secondary border border-border rounded-md text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary">
          <option>全部模块</option>
          <option>用户模块</option>
          <option>商品模块</option>
          <option>订单模块</option>
        </select>
        <select className="px-3 py-2 bg-background-secondary border border-border rounded-md text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary">
          <option>全部状态</option>
          <option>通过</option>
          <option>失败</option>
          <option>执行中</option>
        </select>
      </div>

      {/* Table */}
      <div className="card p-0 overflow-hidden">
        <table className="w-full">
          <thead className="bg-background-secondary">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-foreground-secondary uppercase tracking-wider">
                用例名称
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-foreground-secondary uppercase tracking-wider">
                所属模块
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-foreground-secondary uppercase tracking-wider">
                状态
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-foreground-secondary uppercase tracking-wider">
                最后执行
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-foreground-secondary uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {testCases.map((testCase) => (
              <tr key={testCase.id} className="hover:bg-background-secondary transition-colors">
                <td className="px-4 py-4 text-sm font-medium text-foreground">
                  {testCase.name}
                </td>
                <td className="px-4 py-4 text-sm text-foreground-secondary">
                  {testCase.module}
                </td>
                <td className="px-4 py-4">
                  <span className={`px-2 py-1 text-xs font-medium rounded-md ${statusStyles[testCase.status]}`}>
                    {statusLabels[testCase.status]}
                  </span>
                </td>
                <td className="px-4 py-4 text-sm text-foreground-secondary">
                  {testCase.lastRun}
                </td>
                <td className="px-4 py-4 text-right">
                  <button className="p-1 hover:bg-background-tertiary rounded">
                    <MoreHorizontal className="w-4 h-4 text-foreground-secondary" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between">
        <span className="text-sm text-foreground-secondary">显示 1-6 条，共 1,284 条</span>
        <div className="flex gap-1">
          <button className="px-3 py-1.5 text-sm text-foreground-secondary bg-background-secondary rounded-md hover:bg-border">上一页</button>
          <button className="px-3 py-1.5 text-sm text-white bg-primary rounded-md">1</button>
          <button className="px-3 py-1.5 text-sm text-foreground-secondary bg-background-secondary rounded-md hover:bg-border">2</button>
          <button className="px-3 py-1.5 text-sm text-foreground-secondary bg-background-secondary rounded-md hover:bg-border">3</button>
          <button className="px-3 py-1.5 text-sm text-foreground-secondary bg-background-secondary rounded-md hover:bg-border">下一页</button>
        </div>
      </div>
    </div>
  );
}