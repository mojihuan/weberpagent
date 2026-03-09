import type { Task } from '../../types'

export const mockTasks: Task[] = [
  {
    id: '1',
    name: '用户登录测试',
    description: '使用测试账号登录系统，验证登录流程是否正常工作',
    target_url: 'https://example.com/login',
    max_steps: 10,
    status: 'ready',
    created_at: '2026-03-08T10:00:00Z',
    updated_at: '2026-03-08T14:30:00Z',
  },
  {
    id: '2',
    name: '表单提交测试',
    description: '填写并提交用户信息表单，验证数据提交功能',
    target_url: 'https://example.com/form',
    max_steps: 15,
    status: 'ready',
    created_at: '2026-03-07T09:00:00Z',
    updated_at: '2026-03-07T11:00:00Z',
  },
  {
    id: '3',
    name: '搜索功能测试',
    description: '测试搜索框的关键词搜索和结果展示',
    target_url: 'https://example.com/search',
    max_steps: 8,
    status: 'draft',
    created_at: '2026-03-06T14:00:00Z',
    updated_at: '2026-03-06T14:00:00Z',
  },
  {
    id: '4',
    name: '购物车流程测试',
    description: '添加商品到购物车，修改数量，结算流程',
    target_url: 'https://shop.example.com/cart',
    max_steps: 20,
    status: 'ready',
    created_at: '2026-03-05T08:00:00Z',
    updated_at: '2026-03-05T16:00:00Z',
  },
  {
    id: '5',
    name: '用户注册测试',
    description: '新用户注册流程，包括邮箱验证',
    target_url: 'https://example.com/register',
    max_steps: 12,
    status: 'draft',
    created_at: '2026-03-04T10:00:00Z',
    updated_at: '2026-03-04T10:00:00Z',
  },
  {
    id: '6',
    name: '订单查询测试',
    description: '查询历史订单列表和订单详情',
    target_url: 'https://example.com/orders',
    max_steps: 10,
    status: 'ready',
    created_at: '2026-03-03T09:00:00Z',
    updated_at: '2026-03-03T15:00:00Z',
  },
  {
    id: '7',
    name: '个人设置测试',
    description: '修改用户个人信息和偏好设置',
    target_url: 'https://example.com/settings',
    max_steps: 8,
    status: 'ready',
    created_at: '2026-03-02T11:00:00Z',
    updated_at: '2026-03-02T14:00:00Z',
  },
  {
    id: '8',
    name: '消息通知测试',
    description: '测试系统消息和通知的展示与交互',
    target_url: 'https://example.com/notifications',
    max_steps: 6,
    status: 'draft',
    created_at: '2026-03-01T10:00:00Z',
    updated_at: '2026-03-01T10:00:00Z',
  },
]

let nextId = 100

export function generateTaskId(): string {
  return String(nextId++)
}
