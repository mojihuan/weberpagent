import { useState } from 'react';
import { Header } from '../components/layout';
import { Button } from '../components/ui';
import { Sparkles, Globe, Smartphone, Code, Copy, Download, Save } from 'lucide-react';

const testTypes = [
  { id: 'web', label: 'Web测试', icon: Globe },
  { id: 'mobile', label: '移动端测试', icon: Smartphone },
  { id: 'api', label: 'API测试', icon: Code },
];

const sampleCode = `import { test, expect } from '@playwright/test';

test('用户登录流程测试', async ({ page }) => {
  // 导航到登录页面
  await page.goto('/login');

  // 输入用户名和密码
  await page.fill('#username', 'test_user');
  await page.fill('#password', 'password123');

  // 点击登录按钮
  await page.click('#loginBtn');

  // 验证跳转到首页
  await expect(page).toHaveURL('/home');
});`;

export function AIGeneratePage() {
  const [selectedType, setSelectedType] = useState('web');
  const [prompt, setPrompt] = useState('');

  return (
    <div className="space-y-6">
      <Header
        title="AI 测试用例生成"
        subtitle="使用自然语言描述测试场景，AI自动生成测试用例"
      />

      <div className="grid grid-cols-2 gap-6 h-[calc(100vh-200px)]">
        {/* Input Section */}
        <div className="card flex flex-col">
          <label className="text-sm font-medium text-foreground mb-4">
            描述您的测试场景
          </label>

          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="例如：用户在登录页面输入正确的用户名和密码，点击登录按钮后应该跳转到首页并显示欢迎信息..."
            className="flex-1 w-full p-4 bg-background-secondary rounded-md text-sm text-foreground placeholder:text-foreground-muted resize-none focus:outline-none focus:ring-2 focus:ring-primary"
          />

          {/* Test Type Selection */}
          <div className="flex gap-3 mt-4">
            {testTypes.map((type) => (
              <button
                key={type.id}
                onClick={() => setSelectedType(type.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm transition-colors ${
                  selectedType === type.id
                    ? 'bg-primary text-white'
                    : 'bg-background-tertiary text-foreground-secondary hover:bg-border'
                }`}
              >
                <type.icon className="w-4 h-4" />
                {type.label}
              </button>
            ))}
          </div>

          {/* Generate Button */}
          <Button className="mt-4 w-full h-12" icon={<Sparkles className="w-[18px] h-[18px]" />}>
            生成测试用例
          </Button>
        </div>

        {/* Preview Section */}
        <div className="card flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm font-medium text-foreground">生成结果预览</span>
            <div className="flex gap-2">
              <button className="flex items-center gap-1.5 px-3 py-1.5 text-xs text-foreground-secondary bg-background-tertiary rounded-md hover:bg-border">
                <Copy className="w-3.5 h-3.5" />
                复制
              </button>
              <button className="flex items-center gap-1.5 px-3 py-1.5 text-xs text-foreground-secondary bg-background-tertiary rounded-md hover:bg-border">
                <Download className="w-3.5 h-3.5" />
                下载
              </button>
            </div>
          </div>

          {/* Code Preview */}
          <div className="flex-1 bg-[#1E1E2E] rounded-md p-4 overflow-auto">
            <pre className="text-sm font-mono text-[#CDD6F4] whitespace-pre-wrap">{sampleCode}</pre>
          </div>

          {/* Save Button */}
          <Button variant="success" className="mt-4 w-full h-10" icon={<Save className="w-4 h-4" />}>
            保存到测试用例库
          </Button>
        </div>
      </div>
    </div>
  );
}