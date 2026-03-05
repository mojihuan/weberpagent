import { Header } from '../components/layout';
import { StatCard } from '../components/ui';
import { TestTube, CheckCircle, RefreshCw, Sparkles } from 'lucide-react';

type TestStatus = 'passed' | 'failed' | 'running';

interface RecentTest {
  id: number;
  name: string;
  time: string;
  status: TestStatus;
}

const recentTests: RecentTest[] = [
  { id: 1, name: '用户登录流程测试', time: '3分钟前', status: 'passed' },
  { id: 2, name: '商品搜索功能测试', time: '15分钟前', status: 'passed' },
  { id: 3, name: '订单支付流程测试', time: '32分钟前', status: 'failed' },
  { id: 4, name: '用户注册验证测试', time: '1小时前', status: 'running' },
];

const statusColors: Record<TestStatus, string> = {
  passed: 'bg-success',
  failed: 'bg-danger',
  running: 'bg-warning',
};

const statusTextColors: Record<TestStatus, string> = {
  passed: 'text-success',
  failed: 'text-danger',
  running: 'text-warning',
};

const statusLabels: Record<TestStatus, string> = {
  passed: '通过',
  failed: '失败',
  running: '执行中',
};

export function DashboardPage() {
  return (
    <div className="space-y-6">
      <Header title="仪表盘" subtitle="欢迎回来，查看测试概览" />

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <StatCard
          label="总测试用例"
          value="1,284"
          trend={{ value: '+12% 本周', isPositive: true }}
          icon={<TestTube className="w-5 h-5" />}
        />
        <StatCard
          label="通过率"
          value="94.5%"
          trend={{ value: '+2.3% 本周', isPositive: true }}
          icon={<CheckCircle className="w-5 h-5 text-success" />}
          iconColor="text-success"
        />
        <StatCard
          label="自愈次数"
          value="156"
          trend={{ value: '维护成本降低 60%', isPositive: true }}
          icon={<RefreshCw className="w-5 h-5" />}
        />
        <StatCard
          label="AI生成用例"
          value="328"
          trend={{ value: '效率提升 300%', isPositive: true }}
          icon={<Sparkles className="w-5 h-5 text-warning" />}
          iconColor="text-warning"
        />
      </div>

      {/* Chart and Recent Tests */}
      <div className="grid grid-cols-3 gap-4">
        {/* Chart */}
        <div className="col-span-2 card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-foreground">测试趋势</h3>
            <div className="flex gap-2">
              <button className="px-3 py-1 text-xs font-medium bg-primary text-white rounded-md">周</button>
              <button className="px-3 py-1 text-xs font-medium text-foreground-secondary rounded-md hover:bg-background-tertiary">月</button>
              <button className="px-3 py-1 text-xs font-medium text-foreground-secondary rounded-md hover:bg-background-tertiary">年</button>
            </div>
          </div>
          {/* Simple Bar Chart */}
          <div className="h-64 flex items-end gap-2 pt-4">
            {[180, 160, 200, 140, 190, 170, 210].map((height, i) => (
              <div key={i} className="flex-1 bg-primary rounded" style={{ height: `${height}px` }} />
            ))}
          </div>
          <div className="flex gap-2 mt-2">
            {['周一', '周二', '周三', '周四', '周五', '周六', '周日'].map((day) => (
              <div key={day} className="flex-1 text-center text-xs text-foreground-muted">{day}</div>
            ))}
          </div>
        </div>

        {/* Recent Tests */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-foreground">最近测试执行</h3>
            <span className="text-xs text-primary cursor-pointer hover:underline">查看全部</span>
          </div>
          <div className="space-y-3">
            {recentTests.map((test) => (
              <div key={test.id} className="flex items-center gap-3 p-3 bg-background-secondary rounded-md">
                <div className={`w-2 h-2 rounded-full ${statusColors[test.status]}`} />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-foreground truncate">{test.name}</p>
                  <p className={`text-xs ${statusTextColors[test.status]}`}>
                    {test.time} · {statusLabels[test.status]}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}