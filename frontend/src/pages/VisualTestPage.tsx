import { Header } from '../components/layout';
import { Button } from '../components/ui';
import { Plus, Image, GitCompare } from 'lucide-react';

export function VisualTestPage() {
  return (
    <div className="space-y-6">
      <Header
        title="视觉回归测试"
        subtitle="对比基线截图与最新截图，自动识别视觉差异"
        action={
          <Button icon={<Plus className="w-4 h-4" />}>新建视觉测试</Button>
        }
      />

      {/* Comparison Grid */}
      <div className="grid grid-cols-3 gap-4">
        {/* Baseline */}
        <div className="flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-foreground">基线截图</span>
            <span className="text-xs text-foreground-secondary">2024-03-01</span>
          </div>
          <div className="card flex-1 min-h-[400px] flex items-center justify-center">
            <div className="flex flex-col items-center gap-3 text-foreground-muted">
              <Image className="w-12 h-12" />
              <span className="text-sm">登录页面</span>
            </div>
          </div>
        </div>

        {/* Diff */}
        <div className="flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-foreground">差异对比</span>
            <span className="px-2.5 py-1 text-xs font-medium text-white bg-warning rounded-md">
              3 处差异
            </span>
          </div>
          <div className="card flex-1 min-h-[400px] border-2 border-warning flex items-center justify-center bg-[#FFF3CD]">
            <div className="flex flex-col items-center gap-3 text-warning">
              <GitCompare className="w-12 h-12" />
              <span className="text-sm">检测到差异</span>
            </div>
          </div>
        </div>

        {/* Current */}
        <div className="flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-foreground">最新截图</span>
            <span className="text-xs text-foreground-secondary">2024-03-05</span>
          </div>
          <div className="card flex-1 min-h-[400px] flex items-center justify-center">
            <div className="flex flex-col items-center gap-3 text-foreground-muted">
              <Image className="w-12 h-12" />
              <span className="text-sm">登录页面</span>
            </div>
          </div>
        </div>
      </div>

      {/* Test List */}
      <div className="card">
        <h3 className="font-semibold text-foreground mb-4">视觉测试列表</h3>
        <div className="space-y-3">
          {[
            { name: '登录页面', status: 'changed', diffs: 3 },
            { name: '首页', status: 'unchanged', diffs: 0 },
            { name: '商品详情页', status: 'changed', diffs: 1 },
            { name: '购物车页面', status: 'unchanged', diffs: 0 },
          ].map((test, i) => (
            <div
              key={i}
              className="flex items-center justify-between p-4 bg-background-secondary rounded-md"
            >
              <div className="flex items-center gap-3">
                <div
                  className={`w-2 h-2 rounded-full ${
                    test.status === 'changed' ? 'bg-warning' : 'bg-success'
                  }`}
                />
                <span className="text-sm font-medium text-foreground">{test.name}</span>
              </div>
              {test.diffs > 0 && (
                <span className="px-2 py-1 text-xs text-warning bg-warning/10 rounded-md">
                  {test.diffs} 处差异
                </span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}